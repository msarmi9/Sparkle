//
//  SensorView.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 3/20/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI
import CoreMotion
import os.log

// Sensors (not sure if this is necessary)
struct Sensor: Identifiable {
    var id = UUID()
    var name: String
    var image: String
    // can add more properties
}

let Sensors: [Sensor] = [
    Sensor(name: "Accelerometer", image: "speedometer"),
    Sensor(name: "Gyroscope", image: "crop.rotate"),
    Sensor(name: "Decibels", image: "airplayaudio")]


// init sensor data collection
// https://developer.apple.com/documentation/coremotion/getting_processed_device-motion_data
// https://github.com/hsiaoer/MotionTracking/blob/master/MotionTracking%20WatchKit%20Extension/MotionManager.swift
// 2017 core motion keynote https://developer.apple.com/videos/play/wwdc2017/704/

class MotionManager {
    // MARK: Properties
    let motionManager = CMMotionManager()
    let queue = OperationQueue()

    // MARK: App-specific constants
    let sampleInterval = 1.0 / 20

    // MARK: Initialization

    init() {
        // Serial queue for sample handling and calculations.
        queue.maxConcurrentOperationCount = 1
        queue.name = "MotionManagerQueue"
    }

    // MARK: Motion Manager
    func startUpdates() {
        if !motionManager.isDeviceMotionAvailable {
            print("Device Motion is not available.")
            return
        }

        os_log("Start Updates");

        motionManager.deviceMotionUpdateInterval = sampleInterval
        motionManager.startDeviceMotionUpdates(to: queue) { (deviceMotion: CMDeviceMotion?, error: Error?) in
            if error != nil {
                print("Encountered error: \(error!)")
            }

            if deviceMotion != nil {
                self.processDeviceMotion(deviceMotion!)
            }
        }
    }

    func stopUpdates() {
        if motionManager.isDeviceMotionAvailable {
            motionManager.stopDeviceMotionUpdates()
        }
    }

    // MARK: Motion Processing

    func processDeviceMotion(_ deviceMotion: CMDeviceMotion) {
//        gravityStr = String(format: "X: %.1f Y: %.1f Z: %.1f" ,
//                            deviceMotion.gravity.x,
//                            deviceMotion.gravity.y,
//                            deviceMotion.gravity.z)
//        userAccelStr = String(format: "X: %.1f Y: %.1f Z: %.1f" ,
//                           deviceMotion.userAcceleration.x,
//                           deviceMotion.userAcceleration.y,
//                           deviceMotion.userAcceleration.z)
//        rotationRateStr = String(format: "X: %.1f Y: %.1f Z: %.1f" ,
//                              deviceMotion.rotationRate.x,
//                              deviceMotion.rotationRate.y,
//                              deviceMotion.rotationRate.z)
//        attitudeStr = String(format: "r: %.1f p: %.1f y: %.1f" ,
//                                 deviceMotion.attitude.roll,
//                                 deviceMotion.attitude.pitch,
//                                 deviceMotion.attitude.yaw)
//
        let timestamp = Date().timeIntervalSinceReferenceDate

        os_log("Motion: %@, %@, %@, %@, %@, %@, %@, %@, %@, %@, %@, %@, %@",
               String(timestamp),
               String(deviceMotion.gravity.x),
               String(deviceMotion.gravity.y),
               String(deviceMotion.gravity.z),
               String(deviceMotion.userAcceleration.x),
               String(deviceMotion.userAcceleration.y),
               String(deviceMotion.userAcceleration.z),
               String(deviceMotion.rotationRate.x),
               String(deviceMotion.rotationRate.y),
               String(deviceMotion.rotationRate.z),
               String(deviceMotion.attitude.roll),
               String(deviceMotion.attitude.pitch),
               String(deviceMotion.attitude.yaw))
    }

}



// View
struct SensorView: View {
    let motion = MotionManager()
    lazy var readings = motion.startUpdates()
//    print("Now in SensorView")

    var body: some View {
        VStack {
            List(Sensors){ sensor in
                HStack{
                    Image(systemName: sensor.image)
                    Text(sensor.name)
                }
            }
            // CONTINUE DEBUGGIN HERE - get sensor data to print
            // https://stackoverflow.com/questions/59326558/argument-type-does-not-conform-to-expected-type-view-swiftui
            // something having to do with queue? reference apple dev docs



        }
    }
}

struct SensorView_Previews: PreviewProvider {
    static var previews: some View {
        SensorView()
    }
}
