import get_matrices
import numpy as np


def get_MSE(U1, U2, H1, H2, V, A, X, Y, lambda_x, lambda_y, lambda_u, lambda_h, lambda_v):
    e1 = ((U1.dot(U2.T) + H1.dot(H2.T) - A) ** 2).mean()
    e2 = lambda_x * (((U1.dot(V.T) - X) ** 2).mean())
    e3 = lambda_y * (((U2.dot(V.T) - Y) ** 2).mean())
    e4 = lambda_u * ((U1 ** 2).mean() + (U2 ** 2).mean())
    e5 = lambda_h * ((H1 ** 2).mean() + (H2 ** 2).mean())
    e6 = lambda_v * ((V ** 2).mean())
    return e1 + e2 + e3 + e4 + e5 + e6


def start_training(A, X, Y, r, r_, lambda_x, lambda_y, lambda_u, lambda_h, lambda_v, T):
    m = X.shape[0]
    p = X.shape[1]
    n = Y.shape[0]
    U1 = np.random.rand(m, r)
    U2 = np.random.rand(n, r)
    V = np.random.rand(p, r)
    H1 = np.random.rand(m, r_)
    H2 = np.random.rand(n, r_)
    t = 0
    while t <= T:
        t += 1
        tmp1 = lambda_x * (X.T.dot(U1)) + lambda_y * (Y.T.dot(U2))
        tmp2 = V.dot(lambda_x * U1.T.dot(U1) + lambda_y * U2.T.dot(U2) + lambda_v * np.eye(r))
        tmp3 = np.sqrt(np.divide(tmp1, tmp2))
        V = np.multiply(V, tmp3)
        # update V
        tmp1 = A.dot(U2) + lambda_x * X.dot(V)
        tmp2 = (U1.dot(U2.T) + H1.dot(H2.T)).dot(U2) + U1.dot(lambda_x * V.T.dot(V) + lambda_u * np.eye(r))
        tmp3 = np.sqrt(np.divide(tmp1, tmp2))
        U1 = np.multiply(U1, tmp3)
        # update U1
        tmp1 = A.T.dot(U1) + lambda_y * Y.dot(V)
        tmp2 = (U2.dot(U1.T) + H2.dot(H1.T)).dot(U1) + U2.dot(lambda_y * V.T.dot(V) + lambda_u * np.eye(r))
        tmp3 = np.sqrt(np.divide(tmp1, tmp2))
        U2 = np.multiply(U2, tmp3)
        # update U2
        tmp1 = A.dot(H2)
        tmp2 = (U1.dot(U2.T) + H1.dot(H2.T)).dot(H2) + lambda_h*H1
        tmp3 = np.sqrt(np.divide(tmp1, tmp2))
        H1 = np.multiply(H1, tmp3)
        # update H1
        tmp1 = A.T.dot(H1)
        tmp2 = (U2.dot(U1.T) + H2.dot(H1.T)).dot(H1) + lambda_h * H2
        tmp3 = np.sqrt(np.divide(tmp1, tmp2))
        H2 = np.multiply(H2, tmp3)
        # update H2
        error = get_MSE(U1, U2, H1, H2, V, A, X, Y, lambda_x, lambda_y, lambda_u, lambda_h, lambda_v)
        print error
    return [U1, U2, V, H1, H2]


if __name__ == "__main__":
    feature_cluster_path = "../data/Cell_Phones_and_Accessories_5/feature-cluster.txt"
    reviews_path = "../data/Cell_Phones_and_Accessories_5/extractedReviews.txt"
    neg_entries = "../data/Cell_Phones_and_Accessories_5/opinion-lexicon-English/negative-words.txt"
    pos_entries = "../data/Cell_Phones_and_Accessories_5/opinion-lexicon-English/positive-words.txt"
    [lookup_dict, aspect_index] = get_matrices.get_cluster(feature_cluster_path)
    [user_dict, product_dict] = get_matrices.get_reviews(reviews_path)
    [user_index, product_index] = get_matrices.get_index(user_dict, product_dict)
    user_item_matrix = get_matrices.get_user_item_matrix(reviews_path, user_index, product_index)
    user_feature_matrix = get_matrices.get_user_feature_matrix(user_dict, user_index, lookup_dict, aspect_index, 5)
    neg_dict = get_matrices.get_entries(neg_entries, -1)
    pos_dict = get_matrices.get_entries(pos_entries, 1)
    product_feature_matrix = get_matrices.get_product_feature_matrix(product_dict, product_index, lookup_dict, aspect_index, 5,
                                                        neg_dict, pos_dict)
    [U1, U2, V, H1, H2] = start_training(user_item_matrix, user_feature_matrix, product_feature_matrix, 50, 50, 0.1, 0.1, 0.1, 0.1, 0.1, 450)
    print (U1.dot(U2.T) + H1.dot(H2.T))