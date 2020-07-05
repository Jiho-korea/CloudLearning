import zipfile
zip = zipfile.ZipFile("model/model.zip", "w")
zip.write("model/result.model", compress_type=zipfile.ZIP_DEFLATED)
zip.write("model/classes.npy", compress_type=zipfile.ZIP_DEFLATED)
zip.write("model/std_scaler.bin", compress_type=zipfile.ZIP_DEFLATED)
zip.close()
