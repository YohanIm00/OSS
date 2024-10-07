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

    # Plot midterm/final scores as points
    # Set axes' range
    
    
    # Make both scatter plot
    plt.scatter(midterm_kr, final_kr, c='red', marker='.')
    plt.scatter(midterm_en, final_en, c='blue', marker='+')
    # Modify scatter plot's trivial features
    plt.legend(labels=['Korean', 'English'], loc= "upper left")
    plt.xlabel('Midterm scores')
    plt.xlim(0, 125)
    plt.ylabel('Final scores')
    plt.ylim(0, 100)
    plt.grid()

    # TODO) Plot total scores as a histogram

    plt.show()