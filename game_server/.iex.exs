Code.require_file "game.ex"

defmodule Player do
  def init(conn), do: spawn(fn -> loop(conn) end)

  defp loop(conn, state \\ 0) do
    recv = receive do
      {:update, gamestate} ->
        Enum.reduce(Map.values(gamestate), 0, &max/2)
      after
        :rand.uniform(1000) -> 0
    end
    state = max(recv, state) |> max(:rand.uniform(1000))
    send(conn, {:game_data, self(), state})
    loop(conn, state)
  end
end

gn_pid = GameNetwork.init()
players = [Player.init(gn_pid), Player.init(gn_pid), Player.init(gn_pid)]
send(gn_pid, {:players, players})
