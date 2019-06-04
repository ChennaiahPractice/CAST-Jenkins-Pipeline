// vars/CastAnalyisPipeline.groovy
def call (Map config){

  		def build_ok = true
  
		stage ('CAST-Get Pipeline Code') {
			dir('CAST-Scripts') {
			   git branch: 'master', credentialsId: 'cast-serviceid', url: 'https://git.orgx.net/scm/pas/pas-cast-jenkins-pipeline.git'
			}
		}
		
		/*stage ('CAST-Set Assessment Model') {
          if (build_ok) {
			try {
				echo '-- Enable Assessment Model --'
				bat "\"${WORKSPACE}\\CAST-Scripts\\CLI-Scripts\\CMS_ImportAssessmentModel.bat\" \"profile=${config.cmsprofile}\" \"app=${config.appname}\" \"filepath=%WORKSPACE%\\CAST-Scripts\\QualityModels\\CAST 8.3.6 Assessment Model - Standard.pmx\""
			}
			catch (err) {
				echo '*** Assessment model import failed ***'
				echo err
				echo '**************************************'
			}
          } else {
        	echo 'Errors detected... skipping setting Assessment Model'
          }
		}*/
		
		stage ('CAST-Package application') {
          if (build_ok) {
        	try{
				echo '-- Packaging and Delivery of Source Code --'
				bat "\"${WORKSPACE}\\CAST-Scripts\\CLI-Scripts\\CMS_AutomateDelivery.bat\" \"profile=${config.cmsprofile}\" \"app=${config.appname}\" \"fromVersion=${config.dmtpackage}\" \"version=version %BUILD_NUMBER%\""
            } catch (e) {
            	build_ok = false
                echo e.toString()
            }
          } else {
        	echo 'Errors detected... skipping Packaging Application'
          } 
		}
		
		stage ('CAST-Analyse Application') {
          if (build_ok) {
			try{
              	echo '-- Analyze Application --'
              	bat "\"${WORKSPACE}\\CAST-Scripts\\CLI-Scripts\\CMS_Analyze.bat\" \"profile=${config.cmsprofile}\" \"app=${config.appname}\""
            } catch (e) {
            	build_ok = false
                echo e.toString()
            }
          } else {
        	echo 'Errors detected... skipping analyzing application'
          }
		}
		
		stage ('CAST-Generate Snapshot') {
          if (build_ok) {
        	try{
				echo '-- Generate Snapshot --'
				bat "\"${WORKSPACE}\\CAST-Scripts\\CLI-Scripts\\CMS_GenerateSnapshot.bat\" \"profile=${config.cmsprofile}\" \"app=${config.appname}\" \"version=version ${BUILD_NUMBER}\""
            } catch (e) {
            	build_ok = false
                echo e.toString()
            }
          } else {
        	echo 'Errors detected... skipping generating application snapshot'
          }
		}
  
		stage('CAST-Publish Results'){
          if (build_ok) {
              echo "-- Consolidate Snapshot --"        
              withCredentials([usernamePassword(credentialsId: 'CAST-DB-Keys', passwordVariable: 'PWD1', usernameVariable: 'USR1')]) {
                 bat "\"${WORKSPACE}\\CAST-Scripts\\CLI-Scripts\\AAD_ConsolidateSnapshot.bat\" \"measure=${config.measure}\" \"central=${config.central}\" \"password=${PWD1}\""
              }
			
             echo "-- Refreshing cache --"
             withCredentials([usernamePassword(credentialsId: 'xspas-service-account', passwordVariable: 'PWD1', usernameVariable: 'USR1')]) {
                  bat "curl.exe -u ${USR1}:${PWD1} -H \"Accept: application/json\" ${env.CAST_URL}/rest/server/reload"
             }
          } else {
        	echo 'Errors detected... skipping publishing results to Health Dashboard'
          }
		}
	  
		stage('CAST-Publish Jenkins Report'){
          if (build_ok) {
			echo "-- Create CAST Report in Jenkins --"    
			dir('CAST-Report') {
				withCredentials([usernamePassword(credentialsId: 'xspas-service-account', passwordVariable: 'PWD1', usernameVariable: 'USR1')]) {
					bat "python \"${WORKSPACE}\\CAST-Scripts\\RestAPI\\CAST-Results-Report.py\" --connection=${env.CAST_URL}/rest --username=${USR1} --password=${PWD1} --appname=\"${config.appname}\""
				}
			}
				publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: true, reportDir: 'CAST-Report', reportFiles: 'index.html', reportName: 'CAST Analysis Report', reportTitles: ''])
          } else {
        	echo 'Errors detected... skipping publishing Jenkins Report'
          }
		}
  
        stage('CAST-Email Notification'){
            def mailRecipients = "${config.notificationemail}"
            def jobName = ""
            def emailBody = ""
            if (build_ok) {
            	jobName = currentBuild.fullDisplayName + " - COMPLETED SUCCESSFULLY"
                emailBody = """
                  Dear team,
                  <p>
                  The CAST AIP scan for your application completed. <br>
                  To view results, please access dashboard here: ${env.CAST_URL}
                  <p>
                  Regards,
                  <p>
                  PNC CAST Team
                  """
            } else {
              	jobName = currentBuild.fullDisplayName + " - FAILED"
                emailBody = """
                  Dear team,
                  <p>
                  The CAST AIP scan for your application failed. <br>
                  Please contact PNC CAST team to resolve the issue. <br>
                  <p>
                  Regards,
                  <p>
                  PNC CAST Team
                  """
            }

         	emailext body: "${emailBody}",
                mimeType: 'text/html',
                subject: "[Jenkins] ${jobName}",
                to: "${mailRecipients}",
                replyTo: "${mailRecipients}",
                recipientProviders: [[$class: 'CulpritsRecipientProvider']]
        }
		
		/*
		stage('CAST-Check Success'){
			echo "-- Quality Gate - Check Analysis Results --"
			withCredentials([usernamePassword(credentialsId: 'CAST-Dashboard-Keys', passwordVariable: 'PWD1', usernameVariable: 'USR1')]) {
				bat 'python "%WORKSPACE%\\CAST-Scripts\\RestAPI\\CAST-Check-Rule.py" --connection=http://localhost:8080/CAST-Health-Engineering-838/rest --username=%USR1% --password=%PWD1% --appname=Webstore --ruleid=7742'
			}
		}*/
  
        if(build_ok) {
			currentBuild.result = "SUCCESS"
        } else {
			currentBuild.result = "FAILURE"
        }
}
