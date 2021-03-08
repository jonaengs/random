defmodule Lobby do
  def init(owner) do
    id = "123456"
    pid = spawn fn -> loop(owner, [owner]) end
    {id, pid}
  end

  defp loop(owner, players) do
    receive do
      {:start_game, ^owner} ->
        gn_pid = GameNetwork.init(players)
        for player <- players, do: send(player, {:start, gn_pid})
        send(MainController, {:close, self()})
      {:join, new_player} ->
        players = [new_player | players]
        for player <- players, do: send(player, {:join, new_player, players})
        loop(owner, players)
    end
  end
end

defmodule MainController do
  def init do
    pid = spawn fn -> loop() end
    Process.register(pid, __MODULE__)
    pid
  end

  defp loop(lobbies \\ %{}) do
    receive do
      {:create, player} ->
        {lobby_id, lobby_pid} = Lobby.init(player)
        lobbies = Map.put(lobbies, lobby_id, lobby_pid)
        send(player, {:created, lobby_id, lobby_pid})
        IO.inspect(lobby_id, label: "#{GameLogic.proc_name(player)} opened lobby")
        loop(lobbies)
      {:join, lobby_id, player} ->
        lobby = Map.get(lobbies, lobby_id)
        send(lobby, {:join, player})
        IO.inspect(lobby_id, label: "#{GameLogic.proc_name(player)} joined lobby")
        loop(lobbies)
      {:close, lobby_pid} ->
        lobby_id = Map.to_list(lobbies) |> Enum.filter(& elem(&1, 1) == lobby_pid) |> hd
        loop(Map.delete(lobbies, lobby_id))
    end
  end
end
