//
//  SensorView.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 3/20/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI
import CoreMotion
import Combine
import Foundation
import os.log
import Amplify


// init sensor data collection
// https://developer.apple.com/documentation/coremotion/getting_processed_device-motion_data
// https://github.com/hsiaoer/MotionTracking/blob/master/MotionTracking%20WatchKit%20Extension/MotionManager.swift
// 2017 core motion keynote https://developer.apple.com/videos/play/wwdc2017/704/



class MotionManager: ObservableObject {
    // currently just holds sensor data in memory.. may need to save to a file
    private var motionManager: CMMotionManager
    
    @Published
    var x: Double = 0.0
    @Published
    var y: Double = 0.0
    @Published
    var z: Double = 0.0
    
    // read here about growing the size of an array: https://developer.apple.com/documentation/swift/array
    // for now saving as an array of arrays - potentially just make it a long string in future?
    var sensorString: String = "Acceleration_x, Acceleration_y, Acceleration_z, Rotation_x, Rotation_y, Rotation_z\n"
    
    init() {
        self.motionManager = CMMotionManager()
    }
    
    func startUpdates(Hz: TimeInterval) {
        NSLog("starting updates")
        self.motionManager.deviceMotionUpdateInterval = Hz
        self.motionManager.startDeviceMotionUpdates(to: .main) { (sensorData, error) in
            guard error == nil else {
                print(error!)
                return
            }
            if let sensor = sensorData {
                self.x = sensor.userAcceleration.x
                self.y = sensor.userAcceleration.y
                self.z = sensor.userAcceleration.z
                
                // appending to arr
                NSLog(String(sensor.timestamp))
                self.sensorString = self.sensorString +
                                    "\(sensor.userAcceleration.x)," +
                                    "\(sensor.userAcceleration.y)," +
                                    "\(sensor.userAcceleration.z)," +
                                    "\(sensor.rotationRate.x)," +
                                    "\(sensor.rotationRate.y)," +
                                    "\(sensor.rotationRate.z)" +
                                    "\n"
                
            }
        }
    }
    
    func stopUpdates() {
        NSLog("Stopping Updates")
        NSLog("\(self.sensorString)")
        uploadData(dataString: self.sensorString)
        self.motionManager.stopDeviceMotionUpdates()
    }
//    func toCSV()
}

func uploadData(dataString: String) {
    let data = dataString.data(using: .utf8)!
    // create a key with date/time embedded?
    Amplify.Storage.uploadData(key: "sensorTest2.csv", data: data) { (event) in
        switch event {
        case .completed(let data):
            print("Completed: \(data)")
        case .failed(let storageError):
            print("Failed: \(storageError.errorDescription). \(storageError.recoverySuggestion)")
        case .inProcess(let progress):
            print("Progress: \(progress)")
        default:
            break
        }
    }
}


// View
struct ContentView: View {
    @ObservedObject
    var motion: MotionManager

    var body: some View {
        VStack {
            Button(action: {
                self.motion.startUpdates(Hz: 1.0/20)
            }) {
                Text("Start Recording!")
            }
            Spacer().frame(height: 25)
            Button(action: {
                self.motion.stopUpdates()
            }) {
                Text("Stop Recording!")
            }
            Spacer().frame(height: 25)
            Text("Accelerometer data")
            Text("X: \(self.motion.x)")
            Text("Y: \(self.motion.y)")
            Text("Z: \(self.motion.z)")
        }
    }
}

struct SensorView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView(motion: MotionManager())
    }
}
