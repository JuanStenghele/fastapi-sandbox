resource "kubernetes_service_account" "dashboard" {
  metadata {
    name      = "dashboard-viewer"
    namespace = "kube-system"
  }
}

resource "kubernetes_cluster_role" "dashboard_viewer" {
  metadata {
    name = "dashboard-viewer"
  }

  rule {
    api_groups = [""]
    resources  = ["pods", "pods/log", "services", "endpoints", "namespaces", "nodes", "persistentvolumes", "persistentvolumeclaims", "configmaps", "replicationcontrollers", "events"]
    verbs      = ["get", "list", "watch"]
  }

  rule {
    api_groups = ["apps"]
    resources  = ["deployments", "replicasets", "statefulsets", "daemonsets"]
    verbs      = ["get", "list", "watch"]
  }

  rule {
    api_groups = ["batch"]
    resources  = ["jobs", "cronjobs"]
    verbs      = ["get", "list", "watch"]
  }

  rule {
    api_groups = ["networking.k8s.io"]
    resources  = ["ingresses"]
    verbs      = ["get", "list", "watch"]
  }

  rule {
    api_groups = ["storage.k8s.io"]
    resources  = ["storageclasses"]
    verbs      = ["get", "list", "watch"]
  }
}

resource "kubernetes_cluster_role_binding" "dashboard_viewer" {
  metadata {
    name = "dashboard-viewer"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.dashboard_viewer.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.dashboard.metadata[0].name
    namespace = kubernetes_service_account.dashboard.metadata[0].namespace
  }
}

resource "kubernetes_secret" "dashboard_token" {
  metadata {
    name      = "dashboard-viewer-token"
    namespace = "kube-system"
    annotations = {
      "kubernetes.io/service-account.name" = kubernetes_service_account.dashboard.metadata[0].name
    }
  }

  type = "kubernetes.io/service-account-token"
}

resource "aws_ssm_parameter" "dashboard_token" {
  name  = "/${var.app_name}/kubernetes/dashboard-token"
  type  = "SecureString"
  value = kubernetes_secret.dashboard_token.data["token"]
}
