from ml_model.ml_model import MLModel
if __name__ == '__main__':
    model = MLModel()
    data_frame = model.model_init()
    t = model.data_split(data_frame)
    model.train_model(model.classifier, t[0], t[2])
    y_pred = model.test_model(t[1])

    acc = model.test_accuracy(t[3], y_pred)
    print(acc)