defmodule GameLogic do
  def init(network_pid), do: spawn fn -> loop(network_pid, %{}) end

  def proc_name(pid), do: pid |> Process.info(:registered_name) |> elem(1)

  defp print_gamestate(gamestate) do
    gamestate |> Enum.map(fn {k, v} -> "#{proc_name(k)}: #{v}" end) |> Enum.join(", ") |> IO.puts()
  end

  defp loop(network_pid, gamestate) do
    print_gamestate(gamestate)
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

  def init(players) do
    pid = spawn fn -> loop(players, GameLogic.init(self())) end
    Process.send_after(pid, :tick, @tick_rate)
    pid
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
