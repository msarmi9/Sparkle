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


// init sensor data collection
// https://developer.apple.com/documentation/coremotion/getting_processed_device-motion_data
// https://github.com/hsiaoer/MotionTracking/blob/master/MotionTracking%20WatchKit%20Extension/MotionManager.swift
// 2017 core motion keynote https://developer.apple.com/videos/play/wwdc2017/704/



class MotionManager: ObservableObject {
    private var motionManager: CMMotionManager
    
    @Published
    var x: Double = 0.0
    @Published
    var y: Double = 0.0
    @Published
    var z: Double = 0.0
    
    // read here about growing the size of an array: https://developer.apple.com/documentation/swift/array
    // for now saving as an array of arrays - potentially just make it a long string in future?
    var sensorArr = [[Double]]()
    
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
                self.sensorArr.append([sensor.userAcceleration.x,                          sensor.userAcceleration.y,
                                       sensor.userAcceleration.z])
                
            }
        }
    }
    
    func stopUpdates() {
        NSLog("Stopping Updates")
        self.motionManager.stopDeviceMotionUpdates()
    }
//    func toCSV()
}


// View
struct SensorView: View {
    @ObservedObject
    var motion: MotionManager

    var body: some View {
        VStack {
            Button(action: {
                self.motion.startUpdates(Hz: 1.0/20)
            }) {
                Text("Start Recording!")
            }
            Button(action: {
                self.motion.stopUpdates()
            }) {
                Text("Stop Recording!")
            }
            Text("Accelerometer data")
            Text("X: \(self.motion.x)")
            Text("Y: \(self.motion.y)")
            Text("Z: \(self.motion.z)")
        }
    }
}

struct SensorView_Previews: PreviewProvider {
    static var previews: some View {
        SensorView(motion: MotionManager())
    }
}
