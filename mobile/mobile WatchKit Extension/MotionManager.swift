//
//  MotionManager.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 4/7/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import CoreMotion
import WatchConnectivity


// init sensor data collection
// https://developer.apple.com/documentation/coremotion/getting_processed_device-motion_data
// https://github.com/hsiaoer/MotionTracking/blob/master/MotionTracking%20WatchKit%20Extension/MotionManager.swift
// 2017 core motion keynote https://developer.apple.com/videos/play/wwdc2017/704/



class MotionManager: ObservableObject {
    private var motionManager: CMMotionManager
    
    @Published var x: Double = 0.0
    @Published var y: Double = 0.0
    @Published var z: Double = 0.0
    @Published var sensorString: String = ""
    
    let header = "Acceleration_x, Acceleration_y, Acceleration_z, Rotation_x, Rotation_y, Rotation_z\n"
    
    
    init() {
        self.motionManager = CMMotionManager()
        sensorString = self.header
    }
    
    func reset() {
        self.sensorString = self.header
    }
    
    func startUpdates(Hz: TimeInterval, pillCount: String) {
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
    
    func sendMessage(sensorData: [String: String]) {
        // 2
        guard WCSession.default.isReachable else { return }

        // 3
        WCSession.default.sendMessage(
            sensorData,
            replyHandler: { reply in print(reply) },
            errorHandler: { e in
                print("Error sending the message: \(e.localizedDescription)")
        })
    }
    
    func stopUpdates() {
        NSLog("Stopping Updates")
        NSLog("\(self.sensorString)")
        self.motionManager.stopDeviceMotionUpdates()
    }
}
