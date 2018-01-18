import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import time
from sklearn.neighbors import KNeighborsClassifier

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

'''The below algorithm uses 9 datasets of bid/ask behavior (15,842 values)...
 ... to predict the 10th datasets 1,730 values 
 ... generates 99.7% correct predictions'''
input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\period data\\"
session_name = "AI_predict Test "
input_y = []
input_x = []

for i in range(9):
    input_file = pd.read_csv(input_path + session_name + str(i + 1) + "\\" + "Bid_Ask_History.csv", header=0, delimiter=',')
    input_values = input_file._get_numeric_data()
    input_X = input_values.as_matrix()
    for j in input_X:
        input_x.append(j)
    for k in range(len(input_X)):
        input_y.append(input_X[k][1])


test_x = []
test_y = []
session = "AI_predict Test 10\\"
test_file = pd.read_csv(input_path + session + "Bid_Ask_History.csv", header=0, delimiter=',')
test_data = test_file._get_numeric_data()
test_X = test_data.as_matrix()
for i in test_X:
    test_x.append(i)
for i in range(len(test_X)):
    test_y.append(test_X[i][1])

input_X_train = pd.DataFrame(input_x)
input_y_train = input_y
input_X_test = pd.DataFrame(test_x)
input_y_test = test_y
knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
knn.fit(input_X_train, input_y_train)
y_hat = knn.predict(input_X_test)
print("Bid Ask Predictions with 9 datasets")
print("----------------------------------------------------------------------------------")
print("Size of Datasets: " + str(len(input_y)))
print()
print("Actual Values")
print(input_y_test)
print("Number of Values: " + str(len(input_y_test)))
print()
print("Predicted Values")
print(y_hat.tolist())
print("Number of Values: " + str(len(y_hat)))
print()
print(knn.score(input_X_test, input_y_test))
correct_count = 0
wrong_count = 0

for i in range(len(y_hat)):
    if y_hat[i] == input_y_test[i]:
        correct_count = correct_count + 1
    else:
        wrong_count = wrong_count + 1

print()
percent_correct = correct_count/len(y_hat)
print("Correct Predictions: " + str(correct_count))
print("Wrong Predictions: " + str(wrong_count))
print("Percentage of Right Predictions: " + str(percent_correct*100) + "%")
print("-------------------------------------------------------------------------------------------")
print()
print()

trace1 = go.Scatter(
            x=np.array(range(len(input_y_test))),
            y=np.array(input_y_test), name='Actual Amount',
            mode='markers',
            line=dict(color='rgba(152, 0, 0, .8)', width=4),
            marker=dict(size=10, color='rgba(152, 0, 0, .8)'))

trace2 = go.Scatter(
        x=np.array(range(len(y_hat))),
        y=np.array(y_hat), name='Predicted Amount',
        mode='markers',
        line=dict(color='rgba(200, 150, 150, .9)', width=4),
        marker=dict(size=10, color='rgba(200, 150, 150, .9)'))
data = [trace1, trace2]
layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
                           paper_bgcolor='rgb(255,255,255)',
                           title='Bid Ask Predictions (9 datasets)',
                           xaxis=dict(title='Contract Order',
                                      gridcolor='rgb(255,255,255)',
                                      showgrid=True,
                                      showline=False,
                                      showticklabels=True,
                                      tickcolor='rgb(127,127,127)',
                                      ticks='outside',
                                      zeroline=False,
                                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                           yaxis=dict(title='Transaction Amount ($)',
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