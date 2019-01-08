# Projet Intégrateur TAS

## SSH's GPU access:

1. Access in ssh
```bash
ssh <login>@insa-<machine-id>
```
**machine-id**: 10585 10583

Type password of your INSA login

1. **conda** is not available in your terminal, you have to reload the bash:
```bash
source ~/.bashrc
```
Check conda:
```bash
conda --version
```

## Bibliographic
* [**DeepLearning_Preview.pdf**](biblio/DeepLearning_Preview.pdf): Lecture en diagonal pour connaître les problèmes existants en imagerie et les solution/architecture/challenge/open data.
* [**Segmantic_segmentation_review.pdf**](biblio/Semantic_segmentation_review.pdf): L’ensemble d’état de l’art dans semantic segmentation problème. Il est court (2 pages environ à lire), donc l’information est très concis à comprendre, accepter et continuer à lire, on verra en détail.
* [**Layer_CNN.pdf**](biblio/Layer_CNN.pdf): Ce document présente les couches existantes pour employer en CNN, il faut juste de savoir la fonctionnalité de chaque couche.
* [**Visualization_And_Understanding_CNN.pdf**](biblio/Visualization_And_Understanding_CNN.pdf): Comprendre en visuel ce que apprendre à chaque couche, les “features” qu’on parle dans les documents précédents. Très facile à lire (une heure et demi max pour maîtriser).
* [**U-Net.pdf**](biblio/U-Net.pdf), [**Faster_R-CNN.pdf**](biblio/Faster_R-CNN.pdf), [**DenseNet.pdf**](biblio/DenseNet.pdf) : les architectures intéressantes, à lire pour savoir leurs points forts ainsi que leurs limites.