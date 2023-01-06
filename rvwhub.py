#       sudo chmod 777 -R /home/pi/riverwolves/fisiere
if __name__ == '__main__':
    import multiprocessing
    import rvw_web
    import rvw_creier
    # import rvw_api
    # rvw_api.init()

    multiprocessing.freeze_support()

    multiprocessing.Process(target=rvw_creier.start).start()
    multiprocessing.Process(target=rvw_web.start_web).start()