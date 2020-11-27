import time
from include import imagezmq
from include import predictor



impath = '../images/'
imageHub = imagezmq.ImageHub()
p = predictor.Predictor()

while True:
	(rpiName, frame) = imageHub.recv_jpg()
	imageHub.send_reply(b'OK')
	cur_time = time.time()
	fpath = impath + str(cur_time)+'.jpg'
	with open(fpath, 'wb') as f:
		f.write(frame)
	time.sleep(2.0)
	output = p.predict(fpath)
	print(output)



