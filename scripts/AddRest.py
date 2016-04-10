def previous_sp(index, date_matrix, days=1):
    player = date_matrix[index][0]
    date = date_matrix[index][1+days]
    for newi in xrange(len(date_matrix)):
        if date_matrix[newi][0] == player and date_matrix[newi][1] == date:
            oldsp = date_matrix[newi][-1]
            return oldsp
    return 0

def make_lists(min_lag=1, max_lag=4):
    listofsp = [[] for i in xrange(min_lag+1,max_lag+2)]
    for num, lst in enumerate(listofsp):
        for i in xrange(len(date_matrix)):
            lst.append(previous_sp(i, date_matrix, num+1))
    return listofsp

def addcolumns(listofsp):
    for num, lst in enumerate(listofsp):
        df['SP_'+str(num+1)+'dayago'] = pd.Series(lst, index=df.index)

if __name__ == '__main__':
	addcolumns(make_lists(listofsp))