import os
from features import Type

class ViewPosition(object):
    def __init__(self,table_pos,view_pos):
        self.table_pos=table_pos
        self.view_pos=view_pos

class Instance(object):
    def __init__(self,table_name):
        self.table_name=table_name
        self.column_num=self.tuple_num=0
        self.table_num=self.view_num=0
        self.tables=[]
        self.views=[]

    def addTable(self,table):
        self.tables.append(table)
        self.table_num+=1

    def addTables(self,tables):
        for table in tables:
            self.addTable(table)


    def getScore(self):
        path=os.path.dirname(__file__)
        with open(path+'/data/'+self.table_name+'.ltr','w') as f:
            for i in range(self.table_num):
                self.views.extend([ViewPosition(i,view_pos) for view_pos in range(self.tables[i].view_num)])
            for i in range(self.table_num):
                for j in range(self.tables[i].view_num):
                    view=self.tables[i].views[j]
                    f.write(view.output()+'\n')
        cmd='java -jar "'+path+'/jars/RankLib.jar" -load "'+path+'/jars/rank.model" -rank "'+path+'/data/'+self.table_name+'.ltr" -score "'+path+'/data/'+self.table_name+'.score"'
        os.popen(cmd)
        with open(path+'/data/'+self.table_name+'.score') as f:
            i=0
            line=f.readline()
            while line:
                self.tables[self.views[i].table_pos].views[self.views[i].view_pos].score = float(line.split()[-1])
                line=f.readline()
                i += 1
        self.views.sort(key=lambda view:self.tables[view.table_pos].views[view.view_pos].score,reverse=True)


