shleave_acc = [];

for knr = 3:10
    
    kacgen = knr;
    
    leave_shape
    
    length(final_tr_label)
    trainShapeContext

    shleave_acc(end+1) = accuracy;
end


%% 
figure; 

bar(3:10,shleave_acc,0.6)
title('Shape Edge Count vs Accuracy')
xlabel('Shapes with Edge Count in Training')
ylabel('Test Accuracy')
text( 3:10,shleave_acc,num2str(shleave_acc','%0.4f'),'vert','bottom','horiz','center'); 
box off
axis manual
axis([2 11 0 1])