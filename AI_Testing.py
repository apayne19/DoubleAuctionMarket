import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import time
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import recall_score, precision_score
from sklearn.preprocessing import MinMaxScaler

class SpotMarketPrediction(object):

    def __init__(self):
        self.input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\period data\\"
        self.train_sessions = "AI_strat Test "
        self.test_session = "AI_strat Test 6\\"
        self.train_y = []
        self.train_x = []
        self.test_x = []
        self.test_y = []
        self.bid_ask_list = []
        self.prediction_history = []
        self.input_X_train = None
        self.input_y_train = None
        self.input_X_test = None
        self.input_y_test = None
        self.y_hat = None
        self.knn = None
        self.period_splits = None
        self.indices = []
        self.predict_p0_all = []
        self.predict_p0_bid = []
        self.predict_p0_ask = []
        self.predict_p1_all = []
        self.predict_p1_bid = []
        self.predict_p1_ask = []
        self.predict_p2_all = []
        self.predict_p2_bid = []
        self.predict_p2_ask = []
        self.predict_p3_all = []
        self.predict_p3_bid = []
        self.predict_p3_ask = []
        self.predict_p4_all = []
        self.predict_p4_bid = []
        self.predict_p4_ask = []

    def get_data(self):
        for i in range(5):
            train_file = pd.read_csv(self.input_path + self.train_sessions + str(i + 1) + "\\" + "Bid_Ask_History.csv", header=0,
                                     delimiter=',')
            train_values = train_file._get_numeric_data()
            train_X = train_values.as_matrix()
            for j in train_X:
                # train_x.append(j[1:3])  # trader, amt, strategy
                # train_x.append(j)  # time, trader, amt, strategy
                # train_x.append(j[2])  # amt
                self.train_x.append(j[2:3])  # amt, strategy
            for k in range(len(train_X)):
                self.train_y.append(train_X[k][2])  # amt targets

        test_file = pd.read_csv(self.input_path + self.test_session + "Bid_Ask_History.csv", header=0, delimiter=',')

        for i in test_file.as_matrix():
            self.bid_ask_list.append(i[2])
        test_data = test_file._get_numeric_data()
        test_X = test_data.as_matrix()
        for i in test_X:
            # test_x.append(i[1:3])  # trader, amt, strategy
            # test_x.append(i)  # time, trader, amt, strategy
            # test_x.append(i[2])  # amt
            self.test_x.append(i[2:3])  # amt, strategy
        for i in range(len(test_X)):
            self.test_y.append(test_X[i][2])  # amt targets

    def predict_market(self):  # TODO condense back into two lists of bids asks
        self.input_X_train = pd.DataFrame(self.train_x)
        self.input_y_train = self.train_y
        self.input_X_test = pd.DataFrame(self.test_x)
        self.input_y_test = self.test_y
        self.knn = KNeighborsClassifier(weights='distance')
        self.knn.fit(self.input_X_train, self.input_y_train)
        self.y_hat = self.knn.predict(self.input_X_test)

        for i in range(len(self.y_hat)):
            self.prediction_history.append([self.bid_ask_list[i], self.y_hat[i]])

        if len(self.prediction_history)/5 == int:
            self.period_splits = len(self.prediction_history)/5
        else:
            self.period_splits = round(len(self.prediction_history)/5, 0)

        for i in range(6):
            self.indices.append(int(self.period_splits*i))

        self.predict_p0_all.append(self.prediction_history[self.indices[0]:self.indices[1]])
        for i in range(len(self.predict_p0_all[0])):
            if self.predict_p0_all[0][i][0] == 'bid':
                self.predict_p0_bid.append(self.predict_p0_all[0][i][1])
            else:
                self.predict_p0_ask.append(self.predict_p0_all[0][i][1])

        self.predict_p1_all.append(self.prediction_history[self.indices[1]:self.indices[2]])
        for i in range(len(self.predict_p1_all[0])):
            if self.predict_p1_all[0][i][0] == 'bid':
                self.predict_p1_bid.append(self.predict_p1_all[0][i][1])
            else:
                self.predict_p1_ask.append(self.predict_p1_all[0][i][1])

        self.predict_p2_all.append(self.prediction_history[self.indices[2]:self.indices[3]])
        for i in range(len(self.predict_p2_all[0])):
            if self.predict_p2_all[0][i][0] == 'bid':
                self.predict_p2_bid.append(self.predict_p2_all[0][i][1])
            else:
                self.predict_p2_ask.append(self.predict_p2_all[0][i][1])

        self.predict_p3_all.append(self.prediction_history[self.indices[3]:self.indices[4]])
        for i in range(len(self.predict_p3_all[0])):
            if self.predict_p3_all[0][i][0] == 'bid':
                self.predict_p3_bid.append(self.predict_p3_all[0][i][1])
            else:
                self.predict_p3_ask.append(self.predict_p3_all[0][i][1])

        self.predict_p4_all.append(self.prediction_history[self.indices[4]:self.indices[5]])
        for i in range(len(self.predict_p4_all[0])):
            if self.predict_p4_all[0][i][0] == 'bid':
                self.predict_p4_bid.append(self.predict_p4_all[0][i][1])
            else:
                self.predict_p4_ask.append(self.predict_p4_all[0][i][1])

    def give_trader_info(self, period_p, offer_type):
        period_request = period_p
        type_request = offer_type
        if period_request == 0 and type_request == 'bid':
            return self.predict_p0_bid
        elif period_request == 0 and type_request == 'ask':
            return self.predict_p0_ask
        elif period_request == 1 and type_request == 'bid':
            return self.predict_p1_bid
        elif period_request == 1 and type_request == 'ask':
            return self.predict_p1_ask
        elif period_request == 2 and type_request == 'bid':
            return self.predict_p2_bid
        elif period_request == 2 and type_request == 'ask':
            return self.predict_p2_ask
        elif period_request == 3 and type_request == 'bid':
            return self.predict_p3_bid
        elif period_request == 3 and type_request == 'ask':
            return self.predict_p3_ask
        elif period_request == 4 and type_request == 'bid':
            return self.predict_p4_bid
        elif period_request == 4 and type_request == 'ask':
            return self.predict_p4_ask

    def display_info(self):
        print("----------------------------------------------------------------------------------")
        print("Actual Values")
        print(self.input_y_test)
        print("Number of Values: " + str(len(self.input_y_test)))
        print()
        print("Predicted Values")
        print(self.y_hat.tolist())
        print("Number of Values: " + str(len(self.y_hat)))

        correct_count = 0
        count_one_off = 0
        count_rest_off = 0
        for i in range(len(self.y_hat)):
            if self.y_hat[i] == self.input_y_test[i]:
                correct_count = correct_count + 1
            elif self.y_hat[i] == self.input_y_test[i] - 1 or self.y_hat[i] == self.input_y_test[i] + 1:
                count_one_off = count_one_off + 1
            elif self.y_hat[i] != self.input_y_test[i] - 1 or self.y_hat[i] != self.input_y_test[i] + 1:\
                count_rest_off = count_rest_off + 1
        wrong_count = len(self.y_hat) - correct_count
        print()
        percent_correct = correct_count/len(self.y_hat)
        percent_wrong_one = count_one_off/wrong_count
        print("Correct Predictions: " + str(correct_count))
        print("Wrong Predictions: " + str(wrong_count))
        print("Number of Predictions Off by One: " + str(count_one_off))
        print("Number of Predictions Off more than 1: " + str(count_rest_off))
        print("Percentage of Right Predictions: " + str(percent_correct*100) + "%")
        print("Percentage of Wrong Predictions Off by Only One: " + str(percent_wrong_one*100) + "%")
        print("Train Data Score: " + str(self.knn.score(self.input_X_train, self.input_y_train)))
        print("Test Data Score: " + str(self.knn.score(self.input_X_test, self.input_y_test)))
        # precision = precision_score(input_y_test, y_hat, average="weighted")
        # recall = recall_score(input_y_test, y_hat, average="weighted")
        # print("Precision: " + str(precision))  # false positives: guessed true when false
        # print("Recall: " + str(recall))  # false negatives: guessed true when false
        print("-------------------------------------------------------------------------------------------")
        print("Period 1 Predictions")
        print(self.predict_p0_all)
        print(self.predict_p0_bid)
        print(self.predict_p0_ask)
        print()
        print("Period 2 Predictions")
        print(self.predict_p1_all)
        print(self.predict_p1_bid)
        print(self.predict_p1_ask)
        print()
        print("Period 3 Predictions")
        print(self.predict_p2_all)
        print(self.predict_p2_bid)
        print(self.predict_p2_ask)
        print()
        print("Period 4 Predictions")
        print(self.predict_p3_all)
        print(self.predict_p3_bid)
        print(self.predict_p3_ask)
        print()
        print("Period 5 Predictions")
        print(self.predict_p4_all)
        print(self.predict_p4_bid)
        print(self.predict_p4_ask)

    def graph_predictions(self):
        trace1 = go.Scatter(
                    x=np.array(range(len(self.input_y_test))),
                    y=np.array(self.input_y_test), name='Actual Amount',
                    mode='markers',
                    line=dict(color='rgba(152, 0, 0, .8)', width=4),
                    marker=dict(size=10, color='rgba(152, 0, 0, .8)'))

        trace2 = go.Scatter(
                x=np.array(range(len(self.y_hat))),
                y=np.array(self.y_hat), name='Predicted Amount',
                mode='markers',
                line=dict(color='rgba(200, 150, 150, .9)', width=4),
                marker=dict(size=10, color='rgba(200, 150, 150, .9)'))
        data = [trace1, trace2]
        layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
                                   paper_bgcolor='rgb(255,255,255)',
                                   title='Trader Predictions (6 datasets)',
                                   xaxis=dict(title='Order of Data (Start-->Finish)',
                                              gridcolor='rgb(255,255,255)',
                                              showgrid=True,
                                              showline=False,
                                              showticklabels=True,
                                              tickcolor='rgb(127,127,127)',
                                              ticks='outside',
                                              zeroline=False,
                                              titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                                   yaxis=dict(title='Trader ID (22 traders, index start at 0) ',
                                              gridcolor='rgb(255,255,255)',
                                              showgrid=True,
                                              showline=False,
                                              showticklabels=True,
                                              tickcolor='rgb(127,127,127)',
                                              ticks='outside',
                                              zeroline=False,
                                              titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig)



if __name__ == "__main__":
    # TODO see if it would be possible to employ this algorithm to shock markets to equilibrium
    # TODO build AI_trader that uses this algorithm to place better bids/asks

    # '''Below algorithm uses one dataset of bid/ask values...
    # ... uses half the dataset to train, then predicts the other half
    # ... generates about 82% correct predictions'''
    # bid_ask = []
    # input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\period data\\"
    # session = "AI_predict Test 1\\"
    # input_file_1 = pd.read_csv(input_path + session + "Bid_Ask_History.csv", header=0, delimiter=',')
    # input_X = input_file_1._get_numeric_data()
    # input_x = input_X.as_matrix()
    # for i in range(len(input_x)):
    #     bid_ask.append(input_x[i][1])
    # input_y = bid_ask
    #
    # input_X_train = input_x[:-1000]
    # input_y_train = input_y[:-1000]
    # input_X_test = input_x[-1000:]
    # input_y_test = input_y[-1000:]
    # knn = KNeighborsClassifier()
    # knn.fit(input_X_train, input_y_train)
    # y_hat = knn.predict(input_X_test)
    # print("Bid/Ask Predictions with 1 dataset")
    # print("----------------------------------------------------------------------------------------------------")
    # print("Actual Values")
    # print(input_y_test)
    # print("Number of Values: " + str(len(input_y_test)))
    # print()
    # print("Predicted Values")
    # print(y_hat.tolist())
    # print("Number of Values: " + str(len(y_hat)))
    # correct_count = 0
    # wrong_count = 0
    #
    # for i in range(len(y_hat)):
    #     if y_hat[i] == input_y_test[i]:
    #         correct_count = correct_count + 1
    #     else:
    #         wrong_count = wrong_count + 1
    #
    # print()
    # data_used = len(bid_ask) - len(y_hat)
    # percent_data = data_used/len(bid_ask)
    # percent_correct = correct_count/len(y_hat)
    # print("Percentage of Data Used: " + str(percent_data*100) + "%")
    # print("Correct Predictions: " + str(correct_count))
    # print("Wrong Predictions: " + str(wrong_count))
    # print("Percentage of Right Predictions: " + str(percent_correct*100) + "%")
    # print("Train Data Score: " + str(knn.score(input_X_train, input_y_train)))  # how accurate the model is with train data
    # print("Test Data Score: " + str(knn.score(input_X_test, input_y_test)))  # how accurate the model is with test data
    # # precision = precision_score(input_y_test, y_hat, average="weighted")
    # # recall = recall_score(input_y_test, y_hat, average="weighted")
    # # print("Precision: " + str(precision))  # false positives: guessed true when false
    # # print("Recall: " + str(recall))  # false negatives: guessed true when false
    # print("--------------------------------------------------------------------------------------------")
    # print()
    # print()
    #
    # trace1 = go.Scatter(
    #             x=np.array(range(len(input_y_test))),
    #             y=np.array(input_y_test), name='Actual Amount',
    #             mode='markers',
    #             line=dict(color='rgba(152, 0, 0, .8)', width=4),
    #             marker=dict(size=10, color='rgba(152, 0, 0, .8)'))
    # # graph avg transaction per period
    # trace2 = go.Scatter(
    #         x=np.array(range(len(y_hat))),
    #         y=np.array(y_hat), name='Predicted Amount',
    #         mode='markers',
    #         line=dict(color='rgba(200, 150, 150, .9)', width=4),
    #         marker=dict(size=10, color='rgba(200, 150, 150, .9)'))
    # data = [trace1, trace2]
    # layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
    #                            paper_bgcolor='rgb(255,255,255)',
    #                            title='Bid/Ask Predictions (1 Dataset)',
    #                            xaxis=dict(title='Bid/Ask Order',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
    #                            yaxis=dict(title='Bid/Ask Amount ($)',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
    # fig = go.Figure(data=data, layout=layout)
    # py.offline.plot(fig)
    # time.sleep(0.75)
    #
    # '''Below algorithm pulls from one small dataset of contract transaction prices...
    # ... trains with about half the values, then predicts the other half
    # ... only generates about 20% correct predictions'''
    # contract = []
    # input_file_2 = pd.read_csv(input_path + session + "Contract_History.csv", header=0, delimiter=',')
    # input_X = input_file_2._get_numeric_data()
    # input_x = input_X.as_matrix()
    #
    # for i in range(len(input_x)):
    #     contract.append(input_x[i][0])
    # input_y = contract
    #
    # input_X_train = input_x[:-13]
    # input_y_train = input_y[:-13]
    # input_X_test = input_x[-13:]
    # input_y_test = input_y[-13:]
    # knn = KNeighborsClassifier()
    # knn.fit(input_X_train, input_y_train)
    # y_hat = knn.predict(input_X_test)
    # print("Contract Transaction Predictions with 1 dataset")
    # print("----------------------------------------------------------------------------------------------")
    # print("Size of Dataset: " + str(len(input_y)))
    # print()
    # print("Actual Values")
    # print(input_y_test)
    # print("Number of Values: " + str(len(input_y_test)))
    # print()
    # print("Predicted Values")
    # print(y_hat.tolist())
    # print("Number of Values: " + str(len(y_hat)))
    # correct_count = 0
    # wrong_count = 0
    #
    # for i in range(len(y_hat)):
    #     if y_hat[i] == input_y_test[i]:
    #         correct_count = correct_count + 1
    #     else:
    #         wrong_count = wrong_count + 1
    #
    # print()
    # data_used = len(contract) - len(y_hat)
    # percent_data = data_used/len(contract)
    # percent_correct = correct_count/len(y_hat)
    # print("Percentage of Data Used: " + str(percent_data*100) + "%")
    # print("Correct Predictions: " + str(correct_count))
    # print("Wrong Predictions: " + str(wrong_count))
    # print("Percentage of Right Predictions: " + str(percent_correct*100) + "%")
    # print("Train Data Score: " + str(knn.score(input_X_train, input_y_train)))  # how accurate the model is with train data
    # print("Test Data Score: " + str(knn.score(input_X_test, input_y_test)))  # how accurate the model is with test data
    # # precision = precision_score(input_y_test, y_hat, average="weighted")
    # # recall = recall_score(input_y_test, y_hat, average="weighted")
    # # print("Precision: " + str(precision))  # false positives: guessed true when false
    # # print("Recall: " + str(recall))  # false negatives: guessed true when false
    # print("----------------------------------------------------------------------------------------")
    # print()
    # print()
    #
    # trace1 = go.Scatter(
    #             x=np.array(range(len(input_y_test))),
    #             y=np.array(input_y_test), name='Actual Amount',
    #             mode='markers',
    #             line=dict(color='rgba(152, 0, 0, .8)', width=4),
    #             marker=dict(size=10, color='rgba(152, 0, 0, .8)'))
    # # graph avg transaction per period
    # trace2 = go.Scatter(
    #         x=np.array(range(len(y_hat))),
    #         y=np.array(y_hat), name='Predicted Amount',
    #         mode='markers',
    #         line=dict(color='rgba(200, 150, 150, .9)', width=4),
    #         marker=dict(size=10, color='rgba(200, 150, 150, .9)'))
    # data = [trace1, trace2]
    # layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
    #                            paper_bgcolor='rgb(255,255,255)',
    #                            title='Contract Transaction Predictions (1 Dataset)',
    #                            xaxis=dict(title='Contract Order',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
    #                            yaxis=dict(title='Transaction Amount ($)',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
    # fig = go.Figure(data=data, layout=layout)
    # py.offline.plot(fig)
    # time.sleep(0.75)
    #
    # '''Below is code that reads data values from 19 datasets of contract values...
    # ... then predicts the values of the 20th dataset
    # ... generates 84% correct predictions'''
    # input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\period data\\"
    # session_name = "AI_predict Test "
    # input_y = []
    # input_x = []
    #
    # for i in range(19):
    #     input_file = pd.read_csv(input_path + session_name + str(i + 1) + "\\" + "Contract_History.csv", header=0, delimiter=',')
    #     input_values = input_file._get_numeric_data()
    #     input_X = input_values.as_matrix()
    #     for array in input_X:
    #         for value in array:
    #             input_x.append(value)
    #             input_y.append(value)
    #
    # contract = []
    # session = "AI_predict Test 20\\"
    # test_file = pd.read_csv(input_path + session + "Contract_History.csv", header=0, delimiter=',')
    # test_X = test_file._get_numeric_data()
    # test_x = test_X.as_matrix()
    #
    # for i in range(len(test_x)):
    #     contract.append(test_x[i][0])
    #
    # test_y = contract
    # input_X_train = pd.DataFrame(input_x)
    # input_y_train = input_y
    # input_X_test = test_x
    # input_y_test = test_y
    # knn = KNeighborsClassifier()
    # knn.fit(input_X_train, input_y_train)
    # y_hat = knn.predict(input_X_test)
    # print("Contract Transaction Predictions with 19 datasets")
    # print("--------------------------------------------------------------------------------------------")
    # print("Size of Datasets: " + str(len(input_y)))
    # print()
    # print("Actual Values")
    # print(input_y_test)
    # print("Number of Values: " + str(len(input_y_test)))
    # print()
    # print("Predicted Values")
    # print(y_hat.tolist())
    # print("Number of Values: " + str(len(y_hat)))
    #
    # correct_count = 0
    # wrong_count = 0
    #
    # for i in range(len(y_hat)):
    #     if y_hat[i] == input_y_test[i]:
    #         correct_count = correct_count + 1
    #     else:
    #         wrong_count = wrong_count + 1
    #
    # print()
    # percent_correct = correct_count/len(y_hat)
    # print("Correct Predictions: " + str(correct_count))
    # print("Wrong Predictions: " + str(wrong_count))
    # print("Percentage of Right Predictions: " + str(percent_correct*100) + "%")
    # print("Train Data Score: " + str(knn.score(input_X_train, input_y_train)))
    # print("Test Data Score: " + str(knn.score(input_X_test, input_y_test)))
    # # precision = precision_score(input_y_test, y_hat, average="weighted")  # throws ill-defined error???
    # # recall = recall_score(input_y_test, y_hat, average="weighted")  # throws ill-defined error??
    # # print("Precision: " + str(precision))  # false positives: guessed true when false
    # # print("Recall: " + str(recall))  # false negatives: guessed true when false
    # print("-------------------------------------------------------------------------------------------")
    # print()
    # print()
    #
    # trace1 = go.Scatter(
    #             x=np.array(range(len(input_y_test))),
    #             y=np.array(input_y_test), name='Actual Amount',
    #             mode='markers',
    #             line=dict(color='rgba(152, 0, 0, .8)', width=4),
    #             marker=dict(size=10, color='rgba(152, 0, 0, .8)'))
    #
    # trace2 = go.Scatter(
    #         x=np.array(range(len(y_hat))),
    #         y=np.array(y_hat), name='Predicted Amount',
    #         mode='markers',
    #         line=dict(color='rgba(200, 150, 150, .9)', width=4),
    #         marker=dict(size=10, color='rgba(200, 150, 150, .9)'))
    # data = [trace1, trace2]
    # layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
    #                            paper_bgcolor='rgb(255,255,255)',
    #                            title='Transaction Price Predictions (19 Datasets)',
    #                            xaxis=dict(title='Contract Order',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
    #                            yaxis=dict(title='Transaction Amount ($)',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
    # fig = go.Figure(data=data, layout=layout)
    # py.offline.plot(fig)
    # time.sleep(0.75)
    #
    #
    # '''The below algorithm uses 9 datasets of bid/ask behavior (15,842 values)...
    #  ... to predict the 10th datasets 1,730 values
    #  ... generates 99.7% correct predictions
    #  ... only uses AA trading strategy'''
    # input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\period data\\"
    # session_name = "AI_predict Test "
    # input_y = []
    # input_x = []
    #
    # for i in range(9):
    #     input_file = pd.read_csv(input_path + session_name + str(i + 1) + "\\" + "Bid_Ask_History.csv", header=0, delimiter=',')
    #     input_values = input_file._get_numeric_data()
    #     input_X = input_values.as_matrix()
    #     for j in input_X:
    #         input_x.append(j)
    #     for k in range(len(input_X)):
    #         input_y.append(input_X[k][1])
    #
    #
    # test_x = []
    # test_y = []
    # session = "AI_predict Test 10\\"
    # test_file = pd.read_csv(input_path + session + "Bid_Ask_History.csv", header=0, delimiter=',')
    # test_data = test_file._get_numeric_data()
    # test_X = test_data.as_matrix()
    # for i in test_X:
    #     test_x.append(i)
    # for i in range(len(test_X)):
    #     test_y.append(test_X[i][1])
    #
    # input_X_train = pd.DataFrame(input_x)
    # input_y_train = input_y
    # input_X_test = pd.DataFrame(test_x)
    # input_y_test = test_y
    # knn = KNeighborsClassifier()
    # knn.fit(input_X_train, input_y_train)
    # y_hat = knn.predict(input_X_test)
    # print("Bid Ask Predictions with 9 datasets")
    # print("----------------------------------------------------------------------------------")
    # print("Size of Datasets: " + str(len(input_y)))
    # print()
    # print("Actual Values")
    # print(input_y_test)
    # print("Number of Values: " + str(len(input_y_test)))
    # print()
    # print("Predicted Values")
    # print(y_hat.tolist())
    # print("Number of Values: " + str(len(y_hat)))
    #
    # correct_count = 0
    # wrong_count = 0
    #
    # for i in range(len(y_hat)):
    #     if y_hat[i] == input_y_test[i]:
    #         correct_count = correct_count + 1
    #     else:
    #         wrong_count = wrong_count + 1
    #
    # print()
    # percent_correct = correct_count/len(y_hat)
    # print("Correct Predictions: " + str(correct_count))
    # print("Wrong Predictions: " + str(wrong_count))
    # print("Percentage of Right Predictions: " + str(percent_correct*100) + "%")
    # print("Train Data Score: " + str(knn.score(input_X_train, input_y_train)))
    # print("Test Data Score: " + str(knn.score(input_X_test, input_y_test)))
    # # precision = precision_score(input_y_test, y_hat, average="weighted")
    # # recall = recall_score(input_y_test, y_hat, average="weighted")
    # # print("Precision: " + str(precision))  # false positives: guessed true when false
    # # print("Recall: " + str(recall))  # false negatives: guessed true when false
    # print("-------------------------------------------------------------------------------------------")
    # print()
    # print()
    #
    # trace1 = go.Scatter(
    #             x=np.array(range(len(input_y_test))),
    #             y=np.array(input_y_test), name='Actual Amount',
    #             mode='markers',
    #             line=dict(color='rgba(152, 0, 0, .8)', width=4),
    #             marker=dict(size=10, color='rgba(152, 0, 0, .8)'))
    #
    # trace2 = go.Scatter(
    #         x=np.array(range(len(y_hat))),
    #         y=np.array(y_hat), name='Predicted Amount',
    #         mode='markers',
    #         line=dict(color='rgba(200, 150, 150, .9)', width=4),
    #         marker=dict(size=10, color='rgba(200, 150, 150, .9)'))
    # data = [trace1, trace2]
    # layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
    #                            paper_bgcolor='rgb(255,255,255)',
    #                            title='Bid Ask Predictions (9 datasets)',
    #                            xaxis=dict(title='Contract Order',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
    #                            yaxis=dict(title='Transaction Amount ($)',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
    # fig = go.Figure(data=data, layout=layout)
    # py.offline.plot(fig)
    # time.sleep(0.75)
    #
    #
    # '''The below algorithm uses 5 datasets of containing time,trader,bid/ask,amount,strategy ...
    #  ... to predict the strategies used in the 6th dataset
    #  ... Strategy Index  0:AA, 1:GD, 2:PS, 3:ZIP, 4:ZIC
    #  ... generates predictions at about 88.86% accuracy'''
    # input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\period data\\"
    # session_name = "AI_strat Test "
    # input_y = []
    # input_x = []
    #
    # for i in range(5):
    #     input_file = pd.read_csv(input_path + session_name + str(i + 1) + "\\" + "Bid_Ask_History.csv", header=0, delimiter=',')
    #     input_values = input_file._get_numeric_data()
    #     input_X = input_values.as_matrix()
    #     for j in input_X:
    #         input_x.append(j)
    #     for k in range(len(input_X)):
    #         input_y.append(input_X[k][3])
    #
    # test_x = []
    # test_y = []
    # session = "AI_strat Test 6\\"
    # test_file = pd.read_csv(input_path + session + "Bid_Ask_History.csv", header=0, delimiter=',')
    # test_data = test_file._get_numeric_data()  # eliminates strings in dataframe
    # test_X = test_data.as_matrix()  # turns data into matrix
    # for i in test_X:  # turns matrix into list in order to change to pandas dataframe
    #     test_x.append(i)
    # for i in range(len(test_X)):  # appending just strategies into list
    #     test_y.append(test_X[i][3])
    #
    # input_X_train = pd.DataFrame(input_x)
    # print()
    # print("Example of Data Structures Used")
    # print("========================================================================")
    # print("input_X_train")
    # print(input_X_train)
    # print()
    # input_y_train = input_y
    # print("input_y_train")
    # print(input_y_train)
    # print()
    # input_X_test = pd.DataFrame(test_x)
    # print("input_X_test")
    # print(input_X_test)
    # print()
    # input_y_test = test_y
    # print("input_y_test")
    # print(input_y_test)
    # print()
    # print("=========================================================================")
    # print()
    # print()
    # knn = KNeighborsClassifier(n_neighbors=15)  # nearest neighbors is how the data is split into sections???
    # knn.fit(input_X_train, input_y_train)  # computer fits train data to 3-d plot???
    # y_hat = knn.predict(input_X_test)  # predicts based on how close value is to nearest neighbor???
    # print("Strategy Predictions with 6 datasets")
    # print("----------------------------------------------------------------------------------")
    # print("Size of Datasets: " + str(len(input_y)))
    # print()
    # print("Actual Values")
    # print(input_y_test)
    # print("Number of Values: " + str(len(input_y_test)))
    # print()
    # print("Predicted Values")
    # print(y_hat.tolist())
    # print("Number of Values: " + str(len(y_hat)))
    #
    # correct_count = 0
    # wrong_count = 0
    #
    # for i in range(len(y_hat)):
    #     if y_hat[i] == input_y_test[i]:
    #         correct_count = correct_count + 1
    #     else:
    #         wrong_count = wrong_count + 1
    #
    # print()
    # percent_correct = correct_count/len(y_hat)
    # print("Correct Predictions: " + str(correct_count))
    # print("Wrong Predictions: " + str(wrong_count))
    # print("Percentage of Right Predictions: " + str(percent_correct*100) + "%")
    # print("Train Data Score: " + str(knn.score(input_X_train, input_y_train)))  # how accurate the model is with train data
    # print("Test Data Score: " + str(knn.score(input_X_test, input_y_test)))  # how accurate the model is with test data
    # # precision = precision_score(input_y_test, y_hat, average="weighted")
    # # recall = recall_score(input_y_test, y_hat, average="weighted")
    # # print("Precision: " + str(precision))  # false positives: guessed true when false
    # # print("Recall: " + str(recall))  # false negatives: guessed false when true
    # print("-------------------------------------------------------------------------------------------")
    # print()
    # print()
    #
    # trace1 = go.Scatter(
    #             x=np.array(range(len(input_y_test))),
    #             y=np.array(input_y_test), name='Actual',
    #             mode='markers',
    #             line=dict(color='rgba(152, 0, 0, .8)', width=4),
    #             marker=dict(size=10, color='rgba(152, 0, 0, .8)'))
    #
    # trace2 = go.Scatter(
    #         x=np.array(range(len(y_hat))),
    #         y=np.array(y_hat), name='Predicted',
    #         mode='markers',
    #         line=dict(color='rgba(200, 150, 150, .9)', width=4),
    #         marker=dict(size=10, color='rgba(200, 150, 150, .9)'))
    # data = [trace1, trace2]
    # layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
    #                            paper_bgcolor='rgb(255,255,255)',
    #                            title='Strategy Predictions [0:AA, 1:GD, 2:PS, 3:ZIP, 4:ZIC]',
    #                            xaxis=dict(title='Strategy Order',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
    #                            yaxis=dict(title='Strategy Index',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
    # fig = go.Figure(data=data, layout=layout)
    # py.offline.plot(fig)

    # '''The below algorithm uses 5 datasets of bid/ask behavior...
    #  ... to predict the 6th datasets traders
    #  ... uses multiple trading strategies'''
    # input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\period data\\"
    # session_name = "AI_strat Test "
    # input_y = []
    # input_x = []
    #
    # for i in range(5):
    #     train_file = pd.read_csv(input_path + session_name + str(i + 1) + "\\" + "Bid_Ask_History.csv", header=0, delimiter=',')
    #     train_values = train_file._get_numeric_data()
    #     input_X = train_values.as_matrix()
    #     for j in input_X:
    #         # input_x.append(j[1:3])  # trader, amt, strategy
    #         # input_x.append(j)  # time, trader, amt, strategy
    #         # input_x.append(j[2])  # amt
    #         input_x.append(j[2:3])  # amt, strategy
    #     for k in range(len(input_X)):
    #         input_y.append(input_X[k][2])  # amt targets
    #
    #
    # test_x = []
    # test_y = []
    # session = "AI_strat Test 6\\"
    # test_file = pd.read_csv(input_path + session + "Bid_Ask_History.csv", header=0, delimiter=',')
    # bid_ask_list = []
    # for i in test_file.as_matrix():
    #     bid_ask_list.append(i[2])
    # test_data = test_file._get_numeric_data()
    # test_X = test_data.as_matrix()
    # for i in test_X:
    #     # test_x.append(i[1:3])  # trader, amt, strategy
    #     # test_x.append(i)  # time, trader, amt, strategy
    #     # test_x.append(i[2])  # amt
    #     test_x.append(i[2:3])  # amt, strategy
    # for i in range(len(test_X)):
    #     test_y.append(test_X[i][2])  # amt targets
    #
    # input_X_train = pd.DataFrame(input_x)
    # input_y_train = input_y
    # input_X_test = pd.DataFrame(test_x)
    # input_y_test = test_y
    # knn = KNeighborsClassifier(weights='distance')
    # knn.fit(input_X_train, input_y_train)
    # y_hat = knn.predict(input_X_test)
    # prediction_history = []
    # for i in range(len(y_hat)):
    #     prediction_history.append({bid_ask_list[i]: y_hat[i]})
    #
    # print(bid_ask_list)
    # print(prediction_history)  # TODO split into periods etc then build AI Trader
    # period_splits = len(prediction_history)/5
    # if period_splits != int:
    #     period_splits =
    # print("Period 1 Predictions")
    # print(prediction_history[0:431])
    # print("Period 2 Predictions")
    # print(prediction_history[431:862])
    # print(prediction_history[862:1293])
    # print(prediction_history[1293:1724])
    # print(prediction_history[1724:2155])
    # print(prediction_history[2155:2586])
    # print("Trader Predictions with 6 datasets")
    # print("----------------------------------------------------------------------------------")
    # print("Size of Datasets: " + str(len(input_y)))
    # print()
    # print("Actual Values")
    # print(input_y_test)
    # print("Number of Values: " + str(len(input_y_test)))
    # print()
    # print("Predicted Values")
    # print(y_hat.tolist())
    # print("Number of Values: " + str(len(y_hat)))
    #
    # correct_count = 0
    # count_one_off = 0
    # count_rest_off = 0
    # for i in range(len(y_hat)):
    #     if y_hat[i] == input_y_test[i]:
    #         correct_count = correct_count + 1
    #     elif y_hat[i] == input_y_test[i] - 1 or y_hat[i] == input_y_test[i] + 1:
    #         count_one_off = count_one_off + 1
    #     elif y_hat[i] != input_y_test[i] - 1 or y_hat[i] != input_y_test[i] + 1:\
    #         count_rest_off = count_rest_off + 1
    # wrong_count = len(y_hat) - correct_count
    # print()
    # percent_correct = correct_count/len(y_hat)
    # percent_wrong_one = count_one_off/wrong_count
    # print("Correct Predictions: " + str(correct_count))
    # print("Wrong Predictions: " + str(wrong_count))
    # print("Number of Predictions Off by One: " + str(count_one_off))
    # print("Number of Predictions Off more than 1: " + str(count_rest_off))
    # print("Percentage of Right Predictions: " + str(percent_correct*100) + "%")
    # print("Percentage of Wrong Predictions Off by Only One: " + str(percent_wrong_one*100) + "%")
    # print("Train Data Score: " + str(knn.score(input_X_train, input_y_train)))
    # print("Test Data Score: " + str(knn.score(input_X_test, input_y_test)))
    # # precision = precision_score(input_y_test, y_hat, average="weighted")
    # # recall = recall_score(input_y_test, y_hat, average="weighted")
    # # print("Precision: " + str(precision))  # false positives: guessed true when false
    # # print("Recall: " + str(recall))  # false negatives: guessed true when false
    # print("-------------------------------------------------------------------------------------------")
    # print()
    # print()
    #
    # trace1 = go.Scatter(
    #             x=np.array(range(len(input_y_test))),
    #             y=np.array(input_y_test), name='Actual Amount',
    #             mode='markers',
    #             line=dict(color='rgba(152, 0, 0, .8)', width=4),
    #             marker=dict(size=10, color='rgba(152, 0, 0, .8)'))
    #
    # trace2 = go.Scatter(
    #         x=np.array(range(len(y_hat))),
    #         y=np.array(y_hat), name='Predicted Amount',
    #         mode='markers',
    #         line=dict(color='rgba(200, 150, 150, .9)', width=4),
    #         marker=dict(size=10, color='rgba(200, 150, 150, .9)'))
    # data = [trace1, trace2]
    # layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
    #                            paper_bgcolor='rgb(255,255,255)',
    #                            title='Trader Predictions (6 datasets)',
    #                            xaxis=dict(title='Order of Data (Start-->Finish)',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
    #                            yaxis=dict(title='Trader ID (22 traders, index start at 0) ',
    #                                       gridcolor='rgb(255,255,255)',
    #                                       showgrid=True,
    #                                       showline=False,
    #                                       showticklabels=True,
    #                                       tickcolor='rgb(127,127,127)',
    #                                       ticks='outside',
    #                                       zeroline=False,
    #                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
    # fig = go.Figure(data=data, layout=layout)
    # py.offline.plot(fig)
    # time.sleep(0.75)
    prd = SpotMarketPrediction()
    prd.get_data()
    prd.predict_market()
    prd.display_info()
    prd.graph_predictions()
