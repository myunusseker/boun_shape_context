
shapeCount = 100;
expCount = 5;

%tr_percent = 0.7;


final_training = [];
final_test = [];
final_tr_label = [];
final_test_label = [];


finof = find(shapedata(:,1) == round(tr_percent*shapeCount)+1 ,1,'first');

final_training = shapedata(1:(finof-1),5:end);
final_training(:,3:end) = final_training(:,3:end) / 200.0;
final_training(:,1:2) =  normr(final_training(:,1:2));

final_test = shapedata;

final_tr_label = shape_labels(1:(finof-1));
final_test_label = shape_labels;

%Mdl = fitcsvm(final_training,final_tr_label,'Standardize',true,'KernelFunction','rbf','KernelScale','auto')

fftest = final_test(:,5:end);
fftest(:,3:end) = fftest(:,3:end) /200.0 ; 
fftest(:,1:2) = normr(fftest(:,1:2));

%libsvmwrite('scaled_shapes_force.train',double(final_tr_label),sparse(final_training))
%libsvmwrite('scaled_shapes_force.test',double(final_test_label),sparse(fftest))

