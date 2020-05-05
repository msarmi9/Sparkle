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
import Alamofire
// https://jasonzurita.com/bare-minimum-for-apple-watch-communication/
// https://forums.developer.apple.com/thread/125664
// https://gist.github.com/filsv/55febaea46b6d15d6309a7da7296ec3a

func getTimestamp() -> String {
    let now = Date()
    let formatter = DateFormatter()
    formatter.timeZone = TimeZone.current
    formatter.dateFormat = "yyyy-MM-dd_HH:mm:ss"
    let dateString = formatter.string(from: now)
    return dateString
}

extension String {
    var bool: Bool? {
        switch self.lowercased() {
        case "true", "t", "yes", "y", "1":
            return true
        case "false", "f", "no", "n", "0":
            return false
        default:
            return nil
        }
    }
}

func uploadData(dataString: String) -> String {
    let data = dataString.data(using: .utf8)!
    
    // date-embedded key
    let dateString = getTimestamp()
    
    Amplify.Storage.uploadData(key: "\(dateString)_5.csv", data: data) { (event) in
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

// PUT HTTP Alamofire stuff here!
struct flaskResponse: Decodable {
    let pred_string: String
    let pred_type: String
    let pred: Float
}

// exmaple HTTP parameters:
//let parameters: [String: String] = [
//    "id": "1",    // ideally, we are going to want to retrieve this from a different post request
//    "s3_url": "s3://blah/blah",
//    "recording_data": "Acceleration_x, Acceleration_y, Acceleration_z, Rotation_x, Rotation_y, Rotation_z, pill_count\n1,2,3,4,5,6,7\n8,9,10,11,12,13,14",
//    "timestamp": getTimestamp(),
//    "on_time": "1",
//    ]


func sendPost(parameters: [String: String], _ completion: @escaping (String?, String?, Float?) -> Void){
    AF.request("http://twinkle3.us-west-2.elasticbeanstalk.com/send-data",
               method: .post,
               parameters: parameters,
               encoder: JSONParameterEncoder.default).responseDecodable(of: flaskResponse.self) { response in
//                    debugPrint(response)
                guard let flaskresponse = response.value else { return }
                let pred_string = flaskresponse.pred_string
                let pred_type = flaskresponse.pred_type
                let pred = flaskresponse.pred
                NSLog("Successfully received a response with\npred_string: \(pred_string)\npred: \(pred)")
                completion(pred_string, pred_type, pred)
    }
}

func bool2string(b: Bool) -> String {
    if b == true {
        return "1"
    } else {
        return "0"
    }
}

// NSObject is a base class for ObjC objects
final class WatchSessionManager: NSObject, ObservableObject {
    @Published var messagesReceived: [Message] = []
    
    @Published var pred_string: String = "You haven't taken medication recently."
    @Published var pred_type: String = "N/A"
    @Published var pred: Float = 0.0
    
    @Published var prescription_id: String = ""
    @Published var s3_url: String = ""
    @Published var recording_data: String = ""
    @Published var timestamp: String = ""
    @Published var onTime: Bool = true
    
    //                "id": "7",
    //                "s3_url": "s3://blah/blah/\(getTimestamp())",
    //                "recording_data": String(m["sensorString"] ?? "nil"),
    //                "timestamp": getTimestamp(),
    //                "on_time": "0",
    
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
            
            // now receiving and uploading sensordata to s3
            let sensorString = String(m["sensorString"] ?? "nil")
            let dateString = uploadData(dataString: sensorString)
            
            // send post request
            let parameters = [
                "id": "\(self.prescription_id)",
                "s3_url": "s3://blah/blah/\(getTimestamp())",
                "recording_data": String(m["sensorString"] ?? "nil"),
                "timestamp": getTimestamp(),
                "on_time": bool2string(b: self.onTime),
                ]
            sendPost(parameters: parameters) { pred_string, pred_type, pred  in
                guard let pred_string = pred_string else { return }
                guard let pred_type = pred_type else { return }
                guard let pred = pred else { return }
                self.pred_string = pred_string
                self.pred_type = pred_type
                self.pred = pred
            }
            
            
            // updated UI
            self.messagesReceived.append(Message(dateString: dateString + ".csv"))
            
        }
    }
}




struct SensorLogView: View {
    @ObservedObject
    var watchSession: WatchSessionManager
    // change parameters here!
    var body: some View {
        ScrollView {
            VStack {
                TextField("Prescription id",
                          text: $watchSession.prescription_id)
                Toggle("Intake on time", isOn: $watchSession.onTime)
                Text("Status:").bold()
                Text(watchSession.pred_string).italic().padding(.bottom, 50)
                Text("Prediction Type:")
                Text(watchSession.pred_type).italic().padding(.bottom, 50)
                List(watchSession.messagesReceived) { message in
                    Text(message.dateString)
                }
            }
        }
    }
}

struct SensorLogView_Previews: PreviewProvider {
    static var previews: some View {
        SensorLogView(watchSession: WatchSessionManager())
    }
}
