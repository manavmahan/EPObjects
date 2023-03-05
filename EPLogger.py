from time import localtime, time, strftime

def FormatTime(time):
    return strftime("%Y-%m-%d %H:%M:%S", time)

class Logger:
    StartTime = time()
    Tasks = dict()

    def StartTask(task, *message):
        t = localtime()
        m = "\t-\t".join(message)
        if task in Logger.Tasks:
            try: task = task.split(':-')[0] + str (int(task.split(':-')[1]) + 1)
            except: task += f':-1'

        Logger.Tasks[task] = dict(
            StartTime = time(),
            FinishTime = None,
            Duration = None,
        )

        print (f'{FormatTime(t)} : Started {task} - {m}')
        return task

    def FinishTask(task, *message):
        m = "\t-\t".join(message)
        t = localtime()

        if task in Logger.Tasks:
            Logger.Tasks[task]['FinishTime'] = time()
            Logger.Tasks[task]['Duration'] = f'{(Logger.Tasks[task]["FinishTime"] - Logger.Tasks[task]["StartTime"]):.0f} seconds'
        
        print (f'{FormatTime(t)} : Finished {task} : {Logger.Tasks[task]["Duration"] if task in Logger.Tasks else None} - {m}')

    def PrintSummary():
        for task in Logger.Tasks:
            print (f'{task} : {Logger.Tasks[task]["Duration"]}')