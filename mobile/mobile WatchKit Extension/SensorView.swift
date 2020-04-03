//
//  SensorView.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 3/20/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI
import CoreMotion
import AVFoundation
import WatchConnectivity


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
    
    let header = "Acceleration_x, Acceleration_y, Acceleration_z, Rotation_x, Rotation_y, Rotation_z\n"
    @Published
    var sensorString: String = ""
    
    init() {
        self.motionManager = CMMotionManager()
        sensorString = self.header
    }
    
    func reset() {
        self.sensorString = self.header
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
        self.motionManager.stopDeviceMotionUpdates()  // stopping updates
        // maybe call self.sendMessage(sensorData: ["sensorString", self.sensorString])
//        self.sensorString = self.header
        // find somewhere to reset header
    }
}


//class AudioSession: ObservableObject {
//
//    init() {
//        self.audioSession = AVAudioSession.sharedInstance()
//    }
//
//    func record() {
//        do {
//            // Set the audio session category, mode, and options.
//            try self.audioSession.setCategory(.record, mode: .measurement, options: [])
//        } catch {
//            print("Failed to set audio session category.")
//        }
//    }
//}



// View
struct SensorView: View {
    @ObservedObject
    var motion: MotionManager

    var body: some View {
        ScrollView {
            VStack {
                Button(action: {
                    self.motion.reset()
                    self.motion.startUpdates(Hz: 1.0/5)
                }) {
                    Text("Start Recording!")
                }
                Button(action: {
                    self.motion.stopUpdates()
                    // we'll want to send the sensorString in message, this is for test
                    self.motion.sendMessage(sensorData: ["x": "\(self.motion.x)",
                        "y": "\(self.motion.y)",
                        "z": "\(self.motion.z)",
                        "sensorString": self.motion.sensorString])
                }) {
                    Text("Stop Recording!")
                }
                Text("Accelerometer readings")
                Text("X: \(self.motion.x)")
                Text("Y: \(self.motion.y)")
                Text("Z: \(self.motion.z)")
//                Text("full: \(self.motion.sensorString)")
            }
        }
    }
}

struct SensorView_Previews: PreviewProvider {
    static var previews: some View {
        SensorView(motion: MotionManager())
    }
}
