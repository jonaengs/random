defmodule DataTypes do
  def int, do: <<131, 97>>
  def float, do: <<131, 70>>
  def string, do: <<>>
end

defmodule TableColumn do
  defstruct [
    :name,
    :type,
    :size,

    unique: false,
    pkey: false,
    fkey: false,
    auto_incr: false,
  ]

  def new(kwlist) do
    struct!(TableColumn, kwlist)
  end
end

defmodule Table do
  use GenServer

  defstruct [
    :name,
    :columns,
    :tuple_size,
    :data
  ]

  def start_link({name, columns}) do
    GenServer.start_link(__MODULE__, {name, columns}, name: name)
  end

  @impl GenServer
  def init({name, columns}) do
    table = %Table{
      name: name,
      columns: columns,
      tuple_size: Enum.sum(Enum.map(columns, & &1.size)),
      data: <<>>
    }
    {:ok, table}
  end

  defp pad(bin, length), do: bin <> :binary.copy(<<0>>, length - String.length(bin))

  defp unpad(bin), do: String.trim_trailing(bin, <<0>>)

  defp split_at(binary, ixs, acc \\ [])
  defp split_at(binary, [], acc), do: Enum.reverse([binary | acc])
  defp split_at(binary, ixs, acc) do
    {s1, s2} = String.split_at(binary, hd ixs)
    split_at(s2, tl(ixs), [s1 | acc])
  end

  @impl GenServer
  def handle_call({:insert, _cols, values}, _from, table) do
    data = for {v, c} <- Enum.zip(values, table.columns), into: <<>> do
      {col_size, type} = {c.size, c.type}
      binary = String.slice(:erlang.term_to_binary(v), String.length(type), col_size)
      pad(binary, col_size)
    end
    table = update_in(table.data, & &1 <> data)
    {:reply, :ok, table}
  end

  def handle_call({:get, _cols}, _from, table) do
    tuple_size = table.tuple_size
    column_sizes = Enum.map(table.columns, & &1.size)
    column_types = Enum.map(table.columns, & &1.type)
    data = for <<tuple::binary-size(tuple_size) <- table.data>>,
    {val, type} <- Enum.zip(split_at(tuple, column_sizes), column_types),
    into: [] do
      :erlang.binary_to_term(type <> val)
    end
    IO.inspect Enum.take(data, -10)
    {:reply, :ok, table}
  end
end

Table.start_link({
  Employee,
  [TableColumn.new([name: "id", type: DataTypes.int, size: 4, pkey: true, unique: true]),
  TableColumn.new([name: "name", type: DataTypes.string, size: 32]),
  TableColumn.new([name: "salary", type: DataTypes.float, size: 8])]
})

for i <- 1..200 do
  GenServer.call(Employee, {:insert, nil, [i, "jonatan", 250.0]})
end

GenServer.call(Employee, {:get, nil})
