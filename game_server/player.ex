defmodule Player do
  def init(settings), do: spawn fn -> start(settings) end

  defp start(settings) do
    case settings do
      {:join, lobby_id} ->
        send(MainController, {:join, lobby_id, self()})
      :create ->
        send(MainController, {:create, self()})
    end
    {:ok, gn_pid} = lobby_loop()
    game_loop(gn_pid)
  end

  defp lobby_loop(lobby_pid \\ nil) do
    receive do
      {:created, _lobby_id, lobby_pid} ->
        lobby_loop(lobby_pid)
      {:join, _new_player, _players} ->
        lobby_loop(lobby_pid)
      :start_game ->
        send(lobby_pid, {:start_game, self()})
        lobby_loop(lobby_pid)
      {:start, gn_pid} ->
        {:ok, gn_pid}
    end
  end

  defp game_loop(conn, state \\ 0) do
    recv = receive do
      {:update, gamestate} ->
        Enum.max(Map.values(gamestate), fn -> 0 end)
      after
        :rand.uniform(1000) -> state
    end
    state = Enum.max([state, recv, :rand.uniform(1000)])
    send(conn, {:game_data, self(), state})
    game_loop(conn, state)
  end
end
