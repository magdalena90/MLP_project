
library(ggplot2)
library(reshape)

setwd('/home/magdalena/MSc/MLP_project/vgg16_classify/SemClassImgs')

################################ LOAD FILES ################################

all_files = list.files()
txt_files = c()

n = 4
for(file in all_files){
  if(substr(file, nchar(file)-n+1, nchar(file))=='.csv'){
    txt_files = c(txt_files, file)
  }
}

remove(all_files, n, file)

############################### MERGE FILES ################################

classes = c('Animal','Person','Vehicle')
models = c('Assembled','General','Gray','VGG16')

i=1
for(class in classes[3]){
  j=1
  for(model in models){
    print(txt_files[i])
    f = read.csv(txt_files[i])
    print(nrow(f))
    f[model] = f$maxScore
    f$ID = f$X
    f$X = NULL
    f$maxScore = NULL
    f$class = class
    file_name = paste0('f',j)
    assign(file_name, f)
    i = i+1
    j = j+1
  }
  aux1 = merge(f1,f2,by=c('class','ID'))
  aux2 = merge(aux1,f3, by=c('class','ID'))
  aux3 = merge(aux2, f4, by=c('class','ID'))
  df_name = paste0('class',class)
  assign(df_name, aux3)
}

remove(i,j,class,model,df_name,file_name,f,f1,f2,f3,f4,aux1,aux2,aux3)

aux = rbind(classAnimal, classPerson)
scores = rbind(aux, classVehicle)

remove(aux,classAnimal,classPerson,classVehicle,classes,models,txt_files)

############################# ANALYSE RESULTS ##############################
summary(scores[,c('Assembled','General','Gray','VGG16')])

scores$best = colnames(scores[,-c(1,2)])[apply(scores[,-c(1,2)],1,which.max)]

p1 = ggplot(scores, aes(x=best, fill=best)) + geom_bar() +
  coord_flip() + theme_minimal() + xlab('Model') + ylab('Best score count') +
  scale_fill_manual(values=c("#FFCC36", 'gray', '#5C8CD6', '#51BE49')) +
  theme(legend.position='none', axis.ticks.x=element_blank()) 

melt_scores = melt(scores[,-c(2,7)])

p2 = ggplot(melt_scores, aes(variable, value)) + theme_minimal() + xlab('Model') +
  geom_boxplot(aes(fill=variable)) + theme(legend.position='none', 
  axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  scale_fill_manual(values=c('#5C8CD6', '#FFCC36', 'gray', '#51BE49'))

require(gridExtra)
grid.arrange(p1, p2, ncol=2, widths=c(1.5,1))


scores$ones = 1
aggregate_scores = aggregate(scores$ones, by=list(scores$class, scores$best), FUN=sum)
names(aggregate_scores) = c('class','best','count')

ggplot(aggregate_scores, aes(x=class, y=count, fill=best, label=count)) + geom_col() +
  coord_flip() + theme_minimal() + xlab('Class') + ylab('Best score count') +
  scale_fill_manual(values=c("#FFCC36", 'gray', '#5C8CD6', '#51BE49')) +
  theme(legend.position='none', axis.ticks.x=element_blank()) +
  geom_text(position = position_stack(vjust = 0.5))


