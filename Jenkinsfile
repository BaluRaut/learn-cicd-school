// 🎩 The SAME pipeline in the Jenkins (declarative) dialect — lesson 11.
//   ✅ test (matrix) → 📦 build & push → 🛑 approve → 🚚 deploy
// Needs on the controller: Docker Pipeline, JUnit and Pipeline: AWS Steps plugins, plus a
// credential `aws-school-cicd` (IAM keys or, better, a role assumed by the agent).
pipeline {
  agent none
  options { timestamps(); disableConcurrentBuilds() }
  environment {
    AWS_REGION     = 'ap-south-1'
    ECR_REPOSITORY = 'hello-courier'
    EKS_CLUSTER    = 'school-eks'
  }
  stages {
    stage('✅ test') {
      matrix {                                         // lesson 04: three rulers, in parallel
        axes { axis { name 'NODE'; values '20', '22', '24' } }
        agent { docker { image "node:${NODE}-alpine" } }
        stages {
          stage('test') {
            steps {
              dir('app') {
                // Jenkins has no built-in cache step: a persistent agent keeps the workspace
                // (so prepared/ survives between builds); ephemeral agents need the Job Cacher plugin.
                sh 'node prepare.js'
                sh '''node --test --test-reporter=spec  --test-reporter-destination=stdout \
                                  --test-reporter=junit --test-reporter-destination=test-results.xml'''
              }
            }
            post { always { junit 'app/test-results.xml' } }   // lesson 05: the report card
          }
        }
      }
    }
    stage('📦 build & push') {
      when { branch 'main' }
      agent any
      steps {
        withAWS(credentials: 'aws-school-cicd', region: env.AWS_REGION) {
          sh '''
            ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
            REGISTRY="${ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
            IMAGE="${REGISTRY}/${ECR_REPOSITORY}:${GIT_COMMIT}"
            docker build --build-arg APP_VERSION=$(echo "$GIT_COMMIT" | cut -c1-7) -t "$IMAGE" app   # POSIX sh: no ${VAR:0:7}
            docker run -d --rm -p 3000:3000 --name smoke "$IMAGE" && sleep 2 \
              && docker exec smoke wget -qO- localhost:3000/healthz && docker stop smoke
            aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$REGISTRY"
            docker push "$IMAGE"
          '''
        }
      }
    }
    stage('🚚 staging') {
      when { branch 'main' }
      agent any
      steps { script { deployTo('staging') } }
    }
    stage('🛑 approve') {
      when { branch 'main' }
      options { timeout(time: 2, unit: 'DAYS') }
      steps { input message: 'Deploy to production?', ok: 'Approve' }   // the principal's signature
    }
    stage('🚚 production') {
      when { branch 'main' }
      agent any
      steps { script { deployTo('production') } }
    }
  }
}

def deployTo(String namespace) {
  withAWS(credentials: 'aws-school-cicd', region: env.AWS_REGION) {
    sh """
      ACCOUNT=\$(aws sts get-caller-identity --query Account --output text)
      IMAGE="\${ACCOUNT}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPOSITORY}:${env.GIT_COMMIT}"
      aws eks update-kubeconfig --region ${env.AWS_REGION} --name ${env.EKS_CLUSTER}
      sed -i "s|IMAGE_PLACEHOLDER|\${IMAGE}|" k8s/deployment.yaml
      kubectl apply -n ${namespace} -f k8s/
      kubectl rollout status -n ${namespace} deployment/hello-courier --timeout=180s
    """
  }
}
