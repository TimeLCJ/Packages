xyzbgr = np.concatenate((threeD, lefty[0]), axis=2).reshape(-1, 6)
csv = pd.DataFrame(xyzbgr)
csv.to_csv('xyzbgr.csv', header=False, index=False)