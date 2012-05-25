launchctl setenv MAKAHIKI_DATABASE_URL $MAKAHIKI_DATABASE_URL
launchctl setenv MAKAHIKI_ADMIN_INFO $MAKAHIKI_ADMIN_INFO
launchctl unload ~/staging/makahiki2/makahiki/jobs/org.makahiki.staging.update_energy_usage.plist
launchctl load ~/staging/makahiki2/makahiki/jobs/org.makahiki.staging.update_energy_usage.plist
launchctl unload ~/staging/makahiki2/makahiki/jobs/org.makahiki.staging.check_energy_goal.plist
launchctl load ~/staging/makahiki2/makahiki/jobs/org.makahiki.staging.check_energy_goal.plist
launchctl unload ~/staging/makahiki2/makahiki/jobs/org.makahiki.staging.check_water_goal.plist
launchctl load ~/staging/makahiki2/makahiki/jobs/org.makahiki.staging.check_water_goal.plist