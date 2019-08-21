import Worker

wk = Worker.Worker()
wk.laser_open()
wk.move_to(800, 800)
wk.move_to(400, 300)
wk.move_to(0, 200)
wk.move_to(0, 0)
wk.laser_close()
