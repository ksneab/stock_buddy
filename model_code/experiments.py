import time
import torch

def run_LSTM_training(model, epochs, train_inout_seq, loss_function, optimizer):
    for i in range(epochs):
        start_time = time.time()
        for seq, labels in train_inout_seq:
            optimizer.zero_grad()
            model.hidden_cell = (torch.zeros(1, 1, model.hidden_layer_size),
                            torch.zeros(1, 1, model.hidden_layer_size))

            y_pred = model(seq)

            single_loss = loss_function(y_pred, labels)
            single_loss.backward()
            optimizer.step()
        print(f'epoch: {i:3} run time: {time.time() - start_time}')
        print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')

def run_LSTM_eval(model, test_inputs, fut_pred, test_window):
    model.eval()
    for i in range(fut_pred):
        seq = torch.FloatTensor(test_inputs[-test_window:])
        with torch.no_grad():
            model.hidden = (torch.zeros(1, 1, model.hidden_layer_size),
                            torch.zeros(1, 1, model.hidden_layer_size))
            test_inputs.append(model(seq).item())
    return test_inputs