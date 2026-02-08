data "aws_iam_policy" "ebs_csi_policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
}

module "irsa-ebs-csi" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  version = "5.39.0"

  create_role                   = true
  role_name                     = "AmazonEKSTFEBSCSIRole-${module.eks.cluster_name}"
  provider_url                  = module.eks.oidc_provider
  role_policy_arns              = [data.aws_iam_policy.ebs_csi_policy.arn]
  oidc_fully_qualified_subjects = ["system:serviceaccount:kube-system:ebs-csi-controller-sa"]
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.5"

  cluster_name    = "${var.app_name}-eks"
  cluster_version = "1.29"

  vpc_id                                   = module.vpc.vpc_id
  subnet_ids                               = module.vpc.private_subnets
  cluster_endpoint_public_access           = true
  enable_cluster_creator_admin_permissions = true

  eks_managed_node_groups = {
    main = {
      name           = "main-node-group"
      instance_types = ["t3.small"]
      min_size       = 1
      max_size       = 3
      desired_size   = 2
    }
  }

  cluster_addons = {
    aws-ebs-csi-driver = {
      service_account_role_arn = module.irsa-ebs-csi.iam_role_arn
    }
  }
}

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
    name      = "${var.app_name}-service"
    namespace = "default"
  }
}
