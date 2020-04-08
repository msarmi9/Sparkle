//
//  SensorLogView.swift
//  mobile
//
//  Created by Collin Prather on 3/30/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI
import Combine
import Amplify
import WatchConnectivity
// https://jasonzurita.com/bare-minimum-for-apple-watch-communication/
// https://forums.developer.apple.com/thread/125664
// https://gist.github.com/filsv/55febaea46b6d15d6309a7da7296ec3a


func uploadData(dataString: String) -> String {
    let data = dataString.data(using: .utf8)!
    
    // date-embedded key
    let now = Date()
    let formatter = DateFormatter()
    formatter.timeZone = TimeZone.current
    formatter.dateFormat = "yyyy-MM-dd_HH:mm:ss"
    let dateString = formatter.string(from: now)
    
    
    Amplify.Storage.uploadData(key: "\(dateString).csv", data: data) { (event) in
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
    return dateString
}


// struct to display list of messages sent to s3
struct Message: Identifiable {
    var id = UUID()
    var dateString: String
}


// NSObject is a base class for ObjC objects
final class WatchSessionManager: NSObject, ObservableObject {
    @Published
    var x: String = "0.0"
    @Published
    var y: String = "0.0"
    @Published
    var z: String = "0.0"
    
    @Published
    var messagesReceived: [Message] = []
    
    override init() {
        super.init()
        if WCSession.isSupported() {
            let session = WCSession.default
            session.delegate = self
            session.activate()
        }
    }
}

extension WatchSessionManager: WCSessionDelegate {
    
    public func session(_: WCSession, activationDidCompleteWith _: WCSessionActivationState, error: Error?) {
        if let e = error {
            print("Completed activation with error: \(e.localizedDescription)")
        } else {
            print("Completed activation!")
        }
    }

    public func sessionDidBecomeInactive(_: WCSession) { print("session did become inactive") }
    public func sessionDidDeactivate(_: WCSession) { print("session did deactivate") }

    // 4
    public func session(_: WCSession,
                        didReceiveMessage message: [String: Any],
                        replyHandler: @escaping ([String: Any]) -> Void) {
        print("message received! - \(message)")

        // 5
        guard let m = message as? [String: String] else {
            // 6
            replyHandler([
                "response": "poorly formed message",
                "originalMessage": message,
            ])
            return
        }

        // 7
        replyHandler([
            "response": "properly formed message!",
            "originalMessage": m,
        ])

        // 8
        DispatchQueue.main.async {
            // make sure to put on the main queue to update UI!
            self.x = String(m["x"] ?? "nil")
            self.y = String(m["y"] ?? "nil")
            self.z = String(m["z"] ?? "nil")
            
            // now receiving and uploading sensordata to s3
            let sensorString = String(m["sensorString"] ?? "nil")
            let dateString = uploadData(dataString: sensorString)
            self.messagesReceived.append(Message(dateString: dateString))
            
        }
    }
}




struct SensorLogView: View {
    @ObservedObject
    var watchSession: WatchSessionManager
    
    var body: some View {
        List(watchSession.messagesReceived) { message in
            Text(message.dateString)
        }
    }
}

struct SensorLogView_Previews: PreviewProvider {
    static var previews: some View {
        SensorLogView(watchSession: WatchSessionManager())
    }
}
