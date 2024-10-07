import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]

    # 1) Plot midterm/final scores as scatter plot
    # Make both scatter plot
    plt.scatter(midterm_kr, final_kr, label='Korean', color='red', marker='.')
    plt.scatter(midterm_en, final_en, label='English', color='blue', marker='+')
    # Modify scatter plot's trivial features
    plt.legend(loc= "upper left")
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.xlim(0, 125)
    plt.ylim(0, 100)
    plt.grid()
    # Save figure as image file
    plt.savefig('class_score_scatter.png')
    # Display plot
    plt.show()

    # 2) Plot total scores as a histogram
    # Make both histogram plot
    plt.hist(total_kr, bins=range(0, 101, 5), label='Korean', color='red')
    plt.hist(total_en, bins=range(0, 101, 5), label='English', color='purple', alpha=0.4)
    # Modify scatter plot's trivial features
    plt.legend(loc= "upper left")
    plt.xlabel('Total scores')
    plt.ylabel('The number of students')
    plt.xlim(0, 100)
    # Save figure as image file
    plt.savefig('class_score_hist.png')
    # Display plot
    plt.show()