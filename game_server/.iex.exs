Code.require_file "game.ex"
Code.require_file "main.ex"
Code.require_file "player.ex"


MainController.init()

Player.init(:create) |> Process.register(:p1)
Player.init({:join, "123456"}) |> Process.register(:p2)
Player.init({:join, "123456"}) |> Process.register(:p3)

Process.send_after(:p1, :start_game, 3_000)
