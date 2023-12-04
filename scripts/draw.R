require(ggplot2);require(reshape2);require(scales);require(ggpubr);require(tidyr)


df= read.csv('node_count/200000/community_stats.csv')
sum(df$connectivity==0.0)/length(df$connectivity)
nrow(df[df$connectivity == 0,])/nrow(df)


network_params_lfr= read.csv('network_params_lfr.csv')
network_params_lfr$res <- factor(network_params_lfr$res, levels=c("mod", "0.0001", "0.001", "0.01", "0.1", "0.5"))
network_params_lfr$clustering <- factor(network_params_lfr$clustering, levels=c("Empirical", "LFR"))

degree_dists= read.csv('all_degrees.csv')

all_cm_steps_dists= read.csv('all_cm_steps_dists.csv')
all_cm_steps_dists[all_cm_steps_dists$res=="modularity","res"]="mod"
all_cm_steps_dists$res <- factor(all_cm_steps_dists$res, levels=c("mod", "0.0001", "0.001", "0.01", "0.1", "0.5"))
all_cm_steps_dists$step <- factor(all_cm_steps_dists$step, levels=c("pre-CM", "Filter", "post-CM"))

all_cm_dists= read.csv('all_cm_distributions.csv')
all_cm_dists[all_cm_dists$res=="modularity","res"]="mod"
all_cm_dists[all_cm_dists$name=="oc","name"]="open_citations"
all_cm_dists[all_cm_dists$name=="cen","name"]="CEN"
all_cm_dists[all_cm_dists$type=="LFR ground-truth","type"]="LFR ground-truth communities"
all_cm_dists$res <- factor(all_cm_dists$res, levels=c("mod", "0.0001", "0.001", "0.01", "0.1", "0.5"))
all_cm_dists$type <- factor(all_cm_dists$type, levels=c("Original Leiden clustering", "LFR ground-truth communities", "Leiden clustering of LFR"))

ggplot(aes(x=x,y=count,color=type), data=all_cm_steps_dists[all_cm_steps_dists$name=='wiki_topcats',])+
  facet_grid(res~step)+
  scale_x_continuous(trans="log10",name="Cluster size")+
  scale_y_continuous(trans="log10",name="Cluster count")+
  scale_fill_manual(name = "Network type",values=c("Empirical","LFR"))+
  geom_vline(xintercept=10,color="black",lty=2)+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point(alpha=0.55,size=0.4)+
  theme_bw()+
  theme(legend.position = "bottom")+
  guides(color = guide_legend(title = "Network type", override.aes = list(alpha = 1,size=2)))
ggsave("wiki_topcats_steps_r.png",width=6,height = 8) # 'bl_lambert', 'bl_coal', 'bl_taylor0_1', 'bl_taylor0_2'

ggplot(aes(x=degree,y=count,color=type), data=degree_dists)+
  facet_wrap(~name,ncol=2)+
  scale_x_continuous(trans="log10",name="Node degree")+
  scale_y_continuous(trans="log10",name="Node count")+
  scale_fill_manual(name = "Network type",values=c("Empirical","LFR"))+
  #geom_vline(xintercept=10,color="black",lty=2)+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point(alpha=0.55,size=0.4)+
  theme_bw()+
  theme(legend.position = "bottom")+
  guides(color = guide_legend(title = "Network type", override.aes = list(alpha = 1,size=2)))
ggsave("all_degrees.png",width=5,height = 7) # 'bl_lambert', 'bl_coal', 'bl_taylor0_1', 'bl_taylor0_2'

ggplot(aes(x=x,y=count,color=type), data=all_cm_dists)+
  facet_grid(name~res)+
  scale_x_continuous(trans="log10",name="Cluster size")+
  scale_y_continuous(trans="log10",name="Cluster count")+
  scale_fill_manual(name = "Partition")+
  geom_vline(xintercept=10,color="black",lty=2)+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point(alpha=0.4,size=0.4)+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  theme(legend.position = "bottom")+
  guides(color = guide_legend(title = "Partition", override.aes = list(alpha = 1,size=2)))
ggsave("all_cm_distributions.png",width=7.5,height = 7.5) 

ggplot(aes(x=x,y=count,color=type), data=all_cm_dists[all_cm_dists$name=='CEN',])+
  facet_wrap(~res,ncol=3)+
  scale_x_continuous(trans="log10",name="Cluster size")+
  scale_y_continuous(trans="log10",name="Cluster count")+
  scale_fill_manual(name = "Partition")+
  geom_vline(xintercept=10,color="black",lty=2)+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point(alpha=0.4,size=0.4)+
  theme_bw()+
  #theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  guides(color = guide_legend(title = "Partition", override.aes = list(alpha = 1,size=2)))
ggsave("cen_cm_distributions.png",width=7,height = 3) 


ggplot(aes(x=as.factor(res),y=mixing.parameter,color=clustering,group=clustering), data=network_params_lfr)#[network_params_lfr$clustering=='original',])+
  facet_wrap(~network,ncol=4)+
  scale_x_discrete(name="Resolution value")+
  scale_y_continuous(name="Mixing parameter")+
  scale_fill_manual(name = "Clustering")+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point()+geom_line()+
  theme_bw()+
  theme(legend.position = "bottom", panel.spacing.x = unit(5, "mm"))
ggsave("mu_vs_res_separate.pdf",width=5,height = 4)

ggplot(aes(x=as.factor(res),y=mixing.parameter,color=clustering,group=clustering), data=network_params_lfr)+#=network_params_lfr[network_params_lfr$clustering=='original',])+
  facet_wrap(~network,ncol=4)+
  scale_x_discrete(name="Resolution value")+
  scale_y_continuous(name="Mixing Parameter")+
  scale_fill_manual(name = "Clustering")+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point()+geom_line()+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  theme(legend.position = c(.86,.15))+
  guides(color = guide_legend(title = "Clustering", override.aes = list(alpha = 1,size=2)))
  #theme(legend.position = "bottom", panel.spacing.x = unit(5, "mm"))+
  #theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  #guides(color = guide_legend(title = "Clustering", override.aes = list(alpha = 1,size=2)))
ggsave("mu_vs_res_separate.pdf",width=8,height = 4) # 'bl_lambert', 'bl_coal', 'bl_taylor0_1', 'bl_taylor0_2'


ggplot(aes(x=as.factor(res),y=modularity.score,color=clustering,group=clustering), data=network_params_lfr)+#=network_params_lfr[network_params_lfr$clustering=='original',])+
  facet_wrap(~network,ncol=4)+
  scale_x_discrete(name="Resolution value")+
  scale_y_continuous(name="Modularity score")+
  scale_fill_manual(name = "Clustering")+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point()+geom_line()+
  theme_bw()+
  theme(legend.position = "bottom", panel.spacing.x = unit(5, "mm"))+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  theme(legend.position = c(.86,.15)) + 
  guides(color = guide_legend(title = "Clustering", override.aes = list(alpha = 1,size=2)))
ggsave("mod_vs_res_separate.pdf",width=8,height = 4) # 'bl_lambert', 'bl_coal', 'bl_taylor0_1', 'bl_taylor0_2'

ggplot(aes(x=as.factor(res),y=mixing.parameter,color=clustering,group=clustering), data=network_params_lfr)+#=network_params_lfr[network_params_lfr$clustering=='original',])+
  facet_wrap(~network,ncol=4)+
  scale_x_discrete(name="Resolution value")+
  scale_y_continuous(name="Mixing parameter")+
  scale_fill_manual(name = "Clustering")+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point(aes(shape=clustering,color=clustering))+geom_line(aes(linetype=clustering))+
  theme_bw()+
  #theme(legend.position = "bottom", panel.spacing.x = unit(5, "mm"))+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  theme(legend.position = c(.86,.15))
  #guides(color = guide_legend(title = "Clustering", override.aes = list(alpha = 1,size=2)))
ggsave("mu_vs_res_separate.pdf",width=8,height = 4) # 'bl_lambert', 'bl_coal', 'bl_taylor0_1', 'bl_taylor0_2'


ggplot(aes(x=as.factor(res),y=mean.degree,color=clustering,group=clustering), data=network_params_lfr)+#=network_params_lfr[network_params_lfr$clustering=='original',])+
  facet_wrap(~network,ncol=4)+
  scale_x_discrete(name="Resolution value")+
  scale_y_continuous(name="Mixing parameter")+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point()+geom_line()+
  theme_bw()+
  theme(legend.position = "bottom", panel.spacing.x = unit(5, "mm"))
ggsave("deg_vs_res_separate.pdf",width=9,height = 4) # 'bl_lambert', 'bl_coal', 'bl_taylor0_1', 'bl_taylor0_2'

ggplot(aes(x=reorder(network, mean.degree),y=mean.degree,color=clustering,group=clustering), data=network_params_lfr[network_params_lfr$res=='0.01',])+#=network_params_lfr[network_params_lfr$clustering=='original',])+
  scale_x_discrete(name="Network")+
  scale_y_continuous(name="Average degree")+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point()+geom_line()+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  theme_bw()+
  theme(legend.position = "bottom", panel.spacing.x = unit(5, "mm"))
ggsave("deg.pdf",width=8,height = 3) # 'bl_lambert', 'bl_coal', 'bl_taylor0_1', 'bl_taylor0_2'

ggplot(aes(x=reorder(network, mean.degree),y=tau1,color=clustering,group=clustering), data=network_params_lfr[network_params_lfr$res=='0.01',])+#=network_params_lfr[network_params_lfr$clustering=='original',])+
  scale_x_discrete(name="Network")+
  scale_y_continuous(name="Power-law exponent for degree distribution")+
  #stat_smooth(se=F,alpha=1,size=0.4,method="glm",formula=y ~ poly(x, 2))+
  scale_color_brewer(palette = "Dark2")+
  geom_point()+geom_line()+
  theme_bw()+
  theme(legend.position = "bottom", panel.spacing.x = unit(5, "mm"))
  #theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
ggsave("tau1.pdf",width=4,height = 4) # 'bl_lambert', 'bl_coal', 'bl_taylor0_1', 'bl_taylor0_2'



ggplot(aes(x= as.factor(res),y=cluster_size,fill=partition, color=partition), data=res_limit_exps)+
  #facet_wrap(~method,ncol=2)+
  geom_boxplot(outlier.size = 0)+
  stat_summary(fun.data = mean_sdl,position = position_dodge(width=0.75))+
  stat_summary(fun.data = give.n, geom = "text", vjust=-1.5, position = position_dodge(width=0.75), col="black", size=3)+
  scale_y_continuous(name="Cluster size distribution")+
  #scale_x_discrete(name="Number of cliques of size 10")+
  scale_x_discrete(name="Resolution value")+
  scale_fill_brewer(palette="Set2")+
  scale_color_brewer(palette = "Dark2")+
  theme_bw()
ggsave("res_limit_exps_lieden_cpm_varyres_tree.pdf",width=9,height =  4)


ggplot(aes(x=as.factor(n), y=acc_value, fill=partition, color=partition), data=res_limit_exps[!(res_limit_exps$acc_measure=='FPR') & !(res_limit_exps$acc_measure=='FNR'),])+
  facet_wrap(~acc_measure,ncol=2)+
  #geom_line()+
  geom_bar(stat='identity', position = position_dodge2(preserve = "single"))+
  #stat_summary(fun.data = mean_sdl,position = position_dodge(width=0.75))+
  #stat_summary(fun.data = give.n, geom = "text", vjust=-1.5, position = position_dodge(width=0.75), col="black", size=3)+
  scale_y_continuous(name="Accuracy measures")+
  scale_x_discrete(name="Number of cliques of size 10")+
  #scale_x_discrete(name="Resolution value")+
  scale_fill_brewer(palette="Set2")+
  scale_color_brewer(palette = "Dark2")+
  theme_bw()
ggsave("res_limit_exps_lieden_mod_ring.pdf",width=8,height=6)


ggplot(aes(x=as.factor(n), y=acc_value, fill=partition, color=partition), data=res_limit_exps[!(res_limit_exps$acc_measure=='FPR') & !(res_limit_exps$acc_measure=='FNR'),])+
  facet_wrap(~acc_measure,ncol=2)+
  #geom_line()+
  geom_bar(stat='identity', position = position_dodge2(preserve = "single"))+
  #stat_summary(fun.data = mean_sdl,position = position_dodge(width=0.75))+
  #stat_summary(fun.data = give.n, geom = "text", vjust=-1.5, position = position_dodge(width=0.75), col="black", size=3)+
  scale_y_continuous(name="Accuracy measures")+
  scale_x_discrete(name="Number of cliques of size 10")+
  #scale_x_discrete(name="Resolution value")+
  scale_fill_brewer(palette="Set2")+
  scale_color_brewer(palette = "Dark2")+
  theme_bw()
ggsave("res_limit_exps_lieden_mod_ring_all.pdf",width=8,height=6)



ggplot(aes(x=as.factor(n), y=acc_value, fill=partition, color=partition, group=partition), data=res_limit_exps[!(res_limit_exps$acc_measure=='FPR') & !(res_limit_exps$acc_measure=='FNR') & !(res_limit_exps$acc_measure=='Precision')  & !(res_limit_exps$acc_measure=='Recall') & !(res_limit_exps$acc_measure=='NMI'),])+
  facet_wrap(~acc_measure,ncol=3)+
  geom_point()+geom_line()+
  #stat_summary(fun.data = mean_sdl,position = position_dodge(width=0.75))+
  #stat_summary(fun.data = give.n, geom = "text", vjust=-1.5, position = position_dodge(width=0.75), col="black", size=3)+
  scale_y_continuous(name="Accuracy")+
  scale_x_discrete(name="Number of cliques of size 10")+
  #scale_x_discrete(name="Resolution value")+
  coord_cartesian(ylim=c(0,1))+
  scale_fill_brewer(palette="Set2")+
  scale_color_brewer(palette = "Dark2")+
  theme_bw()+
  theme(legend.position = "none", legend.direction = "horizontal",
        axis.title.x = element_blank(),
        axis.text.x = element_text(angle=0))
ggsave("res_limit_exps_lieden_mod_ring_accuracy.pdf",width=6,height=2)




ggplot(aes(x=as.factor(n), y=acc_value, fill=partition, color=partition, group=partition), data=res_limit_exps[!(res_limit_exps$acc_measure=='ARI') & !(res_limit_exps$acc_measure=='AMI') & !(res_limit_exps$acc_measure=='F1-Score') & !(res_limit_exps$acc_measure=='Precision')  & !(res_limit_exps$acc_measure=='Recall') & !(res_limit_exps$acc_measure=='NMI'),])+
  facet_wrap(~acc_measure,ncol=3)+
  geom_point()+geom_line()+
  #stat_summary(fun.data = mean_sdl,position = position_dodge(width=0.75))+
  #stat_summary(fun.data = give.n, geom = "text", vjust=-1.5, position = position_dodge(width=0.75), col="black", size=3)+
  scale_y_continuous(name="Error")+
  scale_x_discrete(name="")+
  #scale_x_discrete(name="Resolution value")+
  #coord_cartesian(ylim=c(0,1))+
  scale_fill_brewer(palette="Set2")+
  scale_color_brewer(palette = "Dark2")+
  theme_bw()+
  theme(legend.position = "none", legend.direction = "horizontal",
        axis.title.x = element_blank(),
        axis.text.x = element_text(angle=0))
ggsave("res_limit_exps_lieden_mod_ring_fpr_fnr.pdf",width=4,height=2)


ggplot(aes(x=as.factor(mu), y=acc_value, fill=partition, color=partition, group=partition), data=res_limit_exps_lfr[!(res_limit_exps$acc_measure=='ARI') & !(res_limit_exps$acc_measure=='AMI') & !(res_limit_exps$acc_measure=='F1-Score') & !(res_limit_exps$acc_measure=='Precision')  & !(res_limit_exps$acc_measure=='Recall') & !(res_limit_exps$acc_measure=='NMI'),])+
  facet_wrap(~acc_measure,ncol=3)+
  geom_point()+geom_line()+
  #stat_summary(fun.data = mean_sdl,position = position_dodge(width=0.75))+
  #stat_summary(fun.data = give.n, geom = "text", vjust=-1.5, position = position_dodge(width=0.75), col="black", size=3)+
  scale_y_continuous(name="Error")+
  scale_x_discrete(name="Mixing parameter (mu)")+
  #scale_x_discrete(name="Resolution value")+
  #coord_cartesian(ylim=c(0,1))+
  scale_fill_brewer(palette="Set2")+
  scale_color_brewer(palette = "Dark2")+
  theme_bw()+
  theme(legend.position = "none", legend.direction = "horizontal")
ggsave("res_limit_exps_lieden_mod_lfr_mu_fpr_fnr.pdf",width=5.5,height=2.5)



ggplot(aes(x=as.factor(mu), y=acc_value, fill=partition, color=partition, group=partition), data=res_limit_exps_lfr[!(res_limit_exps$acc_measure=='FPR') & !(res_limit_exps$acc_measure=='FNR') & !(res_limit_exps$acc_measure=='Precision')  & !(res_limit_exps$acc_measure=='Recall'),])+
  facet_wrap(~acc_measure,ncol=4)+
  geom_point()+geom_line()+
  #stat_summary(fun.data = mean_sdl,position = position_dodge(width=0.75))+
  #stat_summary(fun.data = give.n, geom = "text", vjust=-1.5, position = position_dodge(width=0.75), col="black", size=3)+
  scale_y_continuous(name="Accuracy")+
  scale_x_discrete(name="Mixing parameter (mu)")+
  #scale_x_discrete(name="Resolution value")+
  coord_cartesian(ylim=c(0,1))+
  scale_fill_brewer(palette="Set2")+
  scale_color_brewer(palette = "Dark2")+
  theme_bw()+
  theme(legend.position = "bottom", legend.direction = "horizontal")
ggsave("res_limit_exps_lieden_mod_lfr_mu_accuracy.pdf",width=10,height=3)

