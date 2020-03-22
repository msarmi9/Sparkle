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



class MotionManager: ObservableObject {
    private var motionManager: CMMotionManager
    
    @Published
    var x: Double = 0.0
    @Published
    var y: Double = 0.0
    @Published
    var z: Double = 0.0
    
    init() {
        self.motionManager = CMMotionManager()
        self.motionManager.deviceMotionUpdateInterval = 1.0/60
        self.motionManager.startDeviceMotionUpdates(to: .main) { (sensorData, error) in
            guard error == nil else {
                print(error!)
                return
            }
            if let sensor = sensorData {
                self.x = sensor.userAcceleration.x
                self.y = sensor.userAcceleration.y
                self.z = sensor.userAcceleration.z
            }
        }
    }
}


// View
struct SensorView: View {
    @ObservedObject
    var motion: MotionManager

    var body: some View {
        VStack {
            Text("Accelerometer data")
            Text("X: \(motion.x)")
            Text("Y: \(motion.y)")
            Text("Z: \(motion.z)")
        }
    }
}

struct SensorView_Previews: PreviewProvider {
    static var previews: some View {
        SensorView(motion: MotionManager())
    }
}
