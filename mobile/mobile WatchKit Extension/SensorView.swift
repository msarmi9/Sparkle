//
//  SensorView.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 3/20/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI
import CoreMotion
import WatchConnectivity




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
    
//    func sendMessage(sensorData: [String: String]) {
//        // 2
//        guard WCSession.default.isReachable else { return }
//
//        // 3
//        WCSession.default.sendMessage(
//            sensorData,
//            replyHandler: { reply in print(reply) },
//            errorHandler: { e in
//                print("Error sending the message: \(e.localizedDescription)")
//        })
//    }
    
    func saveToCSV(url: URL) {
        do {
            try self.sensorString.write(to: url, atomically: true, encoding: .utf8)
//            self.reset()
        } catch {
            print(error.localizedDescription)
        }
    }
    
    func stopUpdates() {
        NSLog("Stopping Updates")
        NSLog("\(self.sensorString)")
        self.motionManager.stopDeviceMotionUpdates()
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

func getTimeStamp() -> String {
    let now = Date()
    let formatter = DateFormatter()
    formatter.timeZone = TimeZone.current
    formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
    let dateString = formatter.string(from: now)
    
    return dateString
}


// View
struct SensorView: View {
    @ObservedObject
    var motion: MotionManager
    
    let watchSessionManager = WatchSessionManager()
    
    func getDocumentsDirectory() -> URL {
        // find all possible documents directories for this user
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)

        // just send back the first one, which ought to be the only one
        return paths[0]
    }

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
                    let filename = "\(getTimeStamp()).csv"
                    self.motion.saveToCSV(url: self.getDocumentsDirectory().appendingPathComponent(filename))
                    // now send it to iphone!
                    var transfer_obj = self.watchSessionManager.transferFile(file: URL(fileURLWithPath: filename), metadata: ["dummy": "metadata"])
                    
                    
//                    self.motion.sendMessage(sensorData: ["x": "\(self.motion.x)",
//                        "y": "\(self.motion.y)",
//                        "z": "\(self.motion.z)",
//                        "sensorString": self.motion.sensorString])
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
