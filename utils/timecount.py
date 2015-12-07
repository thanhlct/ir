'''
Time Couting
'''
import resource
import pdb

class TimeStats(object):
    def __init__(self):
        self.init_update()
    
    def init_update(self):
        self.clocks = {}
        self.clocks_temp = {}
    
    def start_clock(self,name):
        self.clocks_temp[name] = self._CPU()

    def check_time(self, name):
        return self._CPU() - self.clocks_temp[name]

    def end_clock(self,name):
        if (name in self.clocks):
            self.clocks[name] += self._CPU() - self.clocks_temp[name]
        else:
            self.clocks[name] = self._CPU() - self.clocks_temp[name]

    def _CPU(self):
        return (resource.getrusage(resource.RUSAGE_SELF).ru_utime+
                resource.getrusage(resource.RUSAGE_SELF).ru_stime)

    def reset_clock(self, name):
        self.clocks[name] = 0
        self.start_clock(name)

    def show_time(self, name, level='second'):
        seconds = self.check_time(name)
        if name in self.clocks.keys():
            seconds = self.clocks[name]
        if level=='day':
            minutes = seconds//60
            hours = minutes//60
            days = hours//24
            hours = hours%24
            minutes = minutes%60
            seconds = seconds%60
            return '%d days %d hours %d minutes %f seconds'%(days, hours, minutes, seconds)
        elif level=='hour':
            minutes = seconds//60
            hours = minutes//60
            minutes = minutes%60
            seconds = seconds%60
            return 'hours %d minutes %f seconds'%(hours, minutes, seconds)
        elif level=='minute':
            minutes = seconds//60
            seconds = seconds%60
            return '%d minutes %f seconds'% (minutes, seconds)
        elif level=='second':
            return '%f seconds'%(seconds)
        else:
            raise RuntimeError('leve=%s unhandled'%level)
            
