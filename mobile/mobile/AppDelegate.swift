//
//  AppDelegate.swift
//  mobile
//
//  Created by Collin Prather on 3/24/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import UIKit
import Amplify
import AWSMobileClient
import AmplifyPlugins

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {



    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        AWSMobileClient.default().initialize { (userState, error) in
                guard error == nil else {
                    print("Error initializing AWSMobileClient. Error: \(error!.localizedDescription)")
                    return
                }
            print("AWSMobileClient initialized, userstate: \(String(describing: userState))")
                
            self.configureAmplifyWithStorage()
                
            }
            return true
        }
    
    func configureAmplifyWithStorage() {
        let storagePlugin = AWSS3StoragePlugin()
        do {
            try Amplify.add(plugin: storagePlugin)
            try Amplify.configure()
            print("Amplify configured with storage plugin")
        } catch {
            print("Failed to initialize Amplify with \(error)")
        }
    }

    // MARK: UISceneSession Lifecycle

    func application(_ application: UIApplication, configurationForConnecting connectingSceneSession: UISceneSession, options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        // Called when a new scene session is being created.
        // Use this method to select a configuration to create the new scene with.
        return UISceneConfiguration(name: "Default Configuration", sessionRole: connectingSceneSession.role)
    }

    func application(_ application: UIApplication, didDiscardSceneSessions sceneSessions: Set<UISceneSession>) {
        // Called when the user discards a scene session.
        // If any sessions were discarded while the application was not running, this will be called shortly after application:didFinishLaunchingWithOptions.
        // Use this method to release any resources that were specific to the discarded scenes, as they will not return.
    }


}

