import SwiftUI

func getTimeStamp() -> String {
    let now = Date()
    let formatter = DateFormatter()
    formatter.timeZone = TimeZone.current
    formatter.dateFormat = "yyyy-MM-dd_HH:mm:ss"
    let dateString = formatter.string(from: now)
    
    return dateString
}

func getTempDirectory() -> String {
//    let tempDirectory = FileManager.default.ur
//    return tempDirectory
}

func getDocumentsDirectory() -> URL {
    // find all possible documents directories for this user
    let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)

    // just send back the first one, which ought to be the only one
    return paths[0]
}

func saveToCSV(payload: String, url: URL) {
        do {
            try payload.write(to: url, atomically: true, encoding: .utf8)
            NSLog("appears to have successfully saved to csv on apple watch.")
//            self.reset()
        } catch {
            print(error.localizedDescription)
        }
    }

let filepath = getTempDirectory() + getTimeStamp() + ".csv"
print(filepath)

saveToCSV(payload: "test payload", url: URL(string: filepath)!)
