%1.将mat数据读进内存
a=load('matlab.mat');
mkdir para/;
sp = a.stereoParams;
cp1 = sp.CameraParameters1;
lim = cp1.IntrinsicMatrix;
rim = a.stereoParams.CameraParameters2.IntrinsicMatrix;
lrd = a.stereoParams.CameraParameters1.RadialDistortion;
rrd = a.stereoParams.CameraParameters2.RadialDistortion;
ltd = a.stereoParams.CameraParameters2.TangentialDistortion;
rtd = a.stereoParams.CameraParameters2.TangentialDistortion;
rc = a.stereoParams.RotationOfCamera2;
tc = a.stereoParams.TranslationOfCamera2;

dlmwrite('para/lim.txt',lim,'precision', '%.20f','delimiter', '\t', 'newline','pc');
dlmwrite('para/lrd.txt',lrd,'precision', '%.20f','delimiter', '\t', 'newline','pc');
dlmwrite('para/ltd.txt',ltd,'precision', '%.20f','delimiter', '\t', 'newline','pc');
dlmwrite('para/rim.txt',rim,'precision', '%.20f','delimiter', '\t', 'newline','pc');
dlmwrite('para/rrd.txt',rrd,'precision', '%.20f','delimiter', '\t', 'newline','pc');
dlmwrite('para/rtd.txt',rtd,'precision', '%.20f','delimiter', '\t', 'newline','pc');
dlmwrite('para/rotation.txt',rc,'precision', '%.20f','delimiter', '\t', 'newline','pc');
dlmwrite('para/translation.txt',tc,'precision', '%.20f','delimiter', '\t', 'newline','pc');