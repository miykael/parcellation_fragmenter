library(corrplot)
library(ggplot2)

# load the data
mat100 <- as.matrix(read.csv('../notebooks/simLbls100.csv', header = F))
mat10 <- as.matrix(read.csv('../notebooks/simLbls10.csv', header = F))
timing <- read.csv('../notebooks/TimingData.csv')

# name the axes of the matrices
method <- rep(c("GMM", "K-Means", "Ward"), each = 10)
dimnames(mat10) <- list(method, method)
dimnames(mat100) <- list(method, method)

# colo palletes
col <- colorRampPalette(c("#67001F", "#B2182B", "#D6604D", "#F4A582",
                           "#FDDBC7", "#FFFFFF", "#D1E5F0", "#92C5DE",
                           "#4393C3", "#2166AC", "#053061"))
Cols <- c("aquamarine4", "#D9541A", "grey50") # left, right, interhemisphere

# plot the two similarity matrices
par(mfrow=c(1,2))
corrplot(mat10, 
         method = "color",
         tl.col = "black",
         tl.cex = 0.8,
         is.corr = F,
         outline = T,
         cl.lim = c(0,1),
         addgrid.col = "grey80",
         cl.pos = "b",
         col = rep(rev(col(50)), 2))

corrplot(mat100,
         method = "color",
         tl.col = "black",
         tl.cex = 0.8,
         is.corr = F,
         outline = T,
         cl.pos = "b",
         addgrid.col = "grey80",
         cl.lim = c(0,1),
         col = rep(rev(col(50)), 2))

# and the timing one
m <- ggplot(aes(size, time, fill = method), data = timing) +
  geom_line(aes(color = method), size = 1.5) +
  geom_point(size = 3, color = "black", pch = 21) +
  scale_y_log10() +
  guides(color = guide_legend(title = "Method"), fill  = guide_legend(title = "Method")) +
  scale_fill_manual(labels = c("GMM", "K-Means", "Ward"), values = Cols) +
  scale_color_manual(labels = c("GMM", "K-Means", "Ward"), values = Cols) +
  labs(y = "Time in seconds (log)", x = "Number of clusters") +
  theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(), 
        panel.background = element_blank(), 
        axis.line = element_line(colour = "black"),
        text = element_text(size = 15))

# to save the m plot as pdf
ggsave('method_times.png',
       plot = m,
       width = 6,
       height = 4,
       units = "in",
       dpi = "retina",
       device = "png")