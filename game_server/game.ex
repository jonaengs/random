defmodule GameLogic do
  def init(network_pid), do: spawn(fn -> loop(network_pid, %{}) end)

  defp loop(network_pid, gamestate) do
    IO.inspect(gamestate)
    receive do
      {:update, player_data} ->
        gamestate = Map.merge(gamestate, player_data)
        send(network_pid, {:updated, gamestate})
        loop(network_pid, gamestate)
    end
  end
end


defmodule GameNetwork do
  @tick_rate 1000

  def init, do: spawn(fn -> start() end)

  defp start do
    receive do
      {:players, players} ->
        Process.send_after(self(), :tick, @tick_rate)
        loop(players, GameLogic.init(self()))
    end
  end

  defp loop(players, game_pid, player_data \\ %{}) do
    receive do
      {:game_data, player, data} ->
        player_data = Map.put(player_data, player, data)
        loop(players, game_pid, player_data)
      {:updated, gamestate} ->
        for player <- players, do: send(player, {:update, gamestate})
        loop(players, game_pid, player_data)
      :tick ->
        send(game_pid, {:update, player_data})
        Process.send_after(self(), :tick, @tick_rate)
        loop(players, game_pid)
    end
  end
end
