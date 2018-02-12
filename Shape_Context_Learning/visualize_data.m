figure; hold on;
scatter(fftest(predicted_test_labels == 1,1),fftest(predicted_test_labels == 1,2));
scatter(fftest(predicted_test_labels == 0,1),fftest(predicted_test_labels == 0,2));
legend('True','False')
title('Predicted Labels')

% hold on;
% critical_pts = fftest(force_predicted_labels ~= shape_labels & sc_predicted_labels == shape_labels,:);
% scatter(critical_pts(:,1),critical_pts(:,2),'*')
% length(critical_pts)
% 
% hold on;
% lol_pts = fftest(force_predicted_labels == shape_labels & sc_predicted_labels ~= shape_labels,:);
% scatter(lol_pts(:,1),lol_pts(:,2),'+')
% length(lol_pts)
%axis manual
%axis([-0.2 0.3 -0.2 0.3])
figure; hold on;
scatter(fftest(final_test_label == 1,1),fftest(final_test_label == 1,2));
scatter(fftest(final_test_label == 0,1),fftest(final_test_label == 0,2));
legend('True','False')
title('Groundtruth Labels')
%axis manual
%axis([-0.2 0.3 -0.2 0.3])

