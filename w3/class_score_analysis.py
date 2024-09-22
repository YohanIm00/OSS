def read_data(filename):
    # 1) Declare data as a list    
    data = []
    
    # 2) Read `filename` as a list of strings first
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # 3) Ignore a line strating with '#'
                temp = [int(num) for num in line.split(',')] # 4) Convert couples of data as integer values
                data.append(temp)
    
    return data

def calc_weighted_average(data_2d, weight):
    # Calculate the weighted averages of each row of `data_2d`
    average = [data_2d[i][0] * weight[0] + data_2d[i][1] * weight[1] for i in range(len(data_2d))]
    
    return average

def analyze_data(data_1d):
    length = len(data_1d)
    
    # 1) Calculate mean of data
    mean = sum(data_1d) / length
    
    # 2) Calculate variance of data
    temp = 0
    for item in data_1d:
        temp += item ** 2
    var = temp / length - mean ** 2
    
    # 3) Calculate median of data
    data_1d.sort()
    if length % 2 == 0:
        median = (data_1d[length // 2 - 1] + data_1d[length // 2]) / 2
    else:
        median = data_1d[length // 2]
    
    return mean, var, median, min(data_1d), max(data_1d)

if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])
    
    # Write the analysis report as a markdown file
    with open('class_score_analysis.md', 'w') as report:
        report.write('### Individual Score\n\n')
        report.write('| Midterm | Final | Average |\n')
        report.write('| ------- | ----- | ----- |\n')
        for ((m_score, f_score), a_score) in zip(data, average):
            report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
        report.write('\n\n\n')

        report.write('### Examination Analysis\n')
        data_columns = {
            'Midterm': [m_score for m_score, _ in data],
            'Final'  : [f_score for _, f_score in data],
            'Average': average }
        for name, column in data_columns.items():
            mean, var, median, min_, max_ = analyze_data(column)
            report.write(f'* {name}\n')
            report.write(f'  * Mean: **{mean:.3f}**\n')
            report.write(f'  * Variance: {var:.3f}\n')
            report.write(f'  * Median: **{median:.3f}**\n')
            report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')