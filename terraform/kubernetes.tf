data "aws_eks_cluster" "cluster" {
  depends_on = [module.eks]

  name = "${var.app_name}-eks"
}

data "aws_eks_cluster_auth" "cluster" {
  depends_on = [module.eks]

  name = "${var.app_name}-eks"
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

data "kubernetes_service" "fastapi_sandbox_service" {
  depends_on = [module.eks]

  metadata {
    name      = "fastapi-sandbox-service"
    namespace = "default"
  }
}
