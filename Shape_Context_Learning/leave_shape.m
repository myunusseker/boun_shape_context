shapeCount = 100;
expCount = 5;

tr_percent = 0.7;


final_training = [];
final_test = [];
final_tr_label = [];
final_test_label = [];

%kacgen = 3;
nge = (shapedata(:,2) == kacgen);

final_training = shapedata(nge,5:end);
final_training(:,1:2) =  normr(final_training(:,1:2));
final_training(:,3:end) = final_training(:,3:end) / 200.0;
final_test = shapedata(~nge,:);

final_tr_label = shape_labels(nge);
final_test_label = shape_labels(~nge);

fftest = final_test(:,5:end);
fftest(:,1:2) = normr(fftest(:,1:2));
fftest(:,3:end) = fftest(:,3:end) /200.0 ;
