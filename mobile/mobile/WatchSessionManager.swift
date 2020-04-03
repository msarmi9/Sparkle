//
//  WatchSessionManager.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 4/3/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import WatchConnectivity
import Amplify

// *************** TO DO *************************
// - edit uploadData to send data csv data from file!
// - When a message is received from the watch, update the observable object to update view!



//func uploadData(dataString: String) -> String {
//    let data = dataString.data(using: .utf8)!
//
//    // date-embedded key
//    let now = Date()
//    let formatter = DateFormatter()
//    formatter.timeZone = TimeZone.current
//    formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
//    let dateString = formatter.string(from: now)
//
//
//    Amplify.Storage.uploadData(key: "\(dateString).csv", data: data) { (event) in
//        switch event {
//        case .completed(let data):
//            print("Completed: \(data)")
//        case .failed(let storageError):
//            print("Failed: \(storageError.errorDescription). \(storageError.recoverySuggestion)")
//        case .inProcess(let progress):
//            print("Progress: \(progress)")
//        default:
//            break
//        }
//    }
//    return dateString
//}

// NSObject is a base class for ObjC objects
class WatchSessionManager: NSObject, WCSessionDelegate, ObservableObject {
    @Published
    var messagesReceived: [Any] = []
    
    func sessionDidBecomeInactive(_: WCSession) { print("session did become inactive") }
    func sessionDidDeactivate(_: WCSession) { print("session did deactivate") }
    
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        if let e = error {
            print("Completed activation with error: \(e.localizedDescription)")
        } else {
            print("Completed activation!")
        }
    }

    static let sharedManager = WatchSessionManager()
    override init() {
        super.init()
    }

    private let session: WCSession? = WCSession.isSupported() ? WCSession.default : nil


    var validSession: WCSession? {

        // paired - the user has to have their device paired to the watch
        // watchAppInstalled - the user must have your watch app installed
        // Note: if the device is paired, but your watch app is not installed
        // consider prompting the user to install it for a better experience
        // Note: the `#if` syntax is from ObjC
        #if os(iOS)
            if let session = session, session.isPaired && session.isWatchAppInstalled {
                return session
            }
        #elseif os(watchOS)
            return session
        #endif
        return nil
    }

    func startSession() {
        session?.delegate = self
        session?.activate()
    }
}


// MARK: Transfer File
extension WatchSessionManager {

    // Sender
    func transferFile(file: URL, metadata: [String : Any]) -> WCSessionFileTransfer? {
        return validSession?.transferFile(file as URL, metadata: metadata)
    }

    func session(_ session: WCSession, didFinish fileTransfer: WCSessionFileTransfer, error: Error?) {
        // handle filed transfer completion
        if let e = error {
            print("Completed file transfer with error: \(e.localizedDescription)")
        } else {
            print("Completed file transfer!")
        }
    }

    func session(_ session: WCSession, didFinishWithError fileTransfer: WCSessionFileTransfer, error: Error?) {
        // handle filed transfer completion
        if let e = error {
            print("runs through the 'didFinishWithError' function")
            print("Completed file transfer with error: \(e.localizedDescription)")
        } else {
            print("Completed file transfer!")
        }
    }

    // Receiver
    func session(_ session: WCSession, didReceive file: WCSessionFile) {
        // handle receiving file
        DispatchQueue.main.async {
            // make sure to put on the main queue to update UI!
        }
    }
}
