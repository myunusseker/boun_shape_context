%% Load Data
shapedata = csvread('/home/yunus/shapeSceneERHAN/shape_data_FORCE_Multiplied.csv');
shapelabels = csvread('/home/yunus/shapeSceneERHAN/shape_labels_FORCE_Multiplied.csv');
shape_labels = shapelabels == 1;

%% 
accurArray = [];
pctArray = [0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9];
for i = 1:9
    tr_percent = pctArray(i);
    divideTrainData
    trainShapeContext

    accurArray(end+1) = accuracy;
end

%%
figure; 

bar((0.1:0.1:0.9),accurArray,0.6)
title('Test Accuracy vs Increasing Amount of Train Data')
xlabel('Percentage of Train Data')
ylabel('Test Accuracy')
text((0.1:0.1:0.9),accurArray,num2str(accurArray','%0.3f'),'vert','bottom','horiz','center'); 
box off
axis manual
axis([0 1 0 1])
