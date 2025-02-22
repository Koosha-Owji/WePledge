import { format } from "date-fns"
import { IChartDataEntry } from "../interfaces/ChartData"
import { IBusinessTripEntry, ICommutingEntry, IElectricityEntry, IHeatingEntry } from "../interfaces/EmissionEntries"

enum backendResultFields {
    BUSINESSTRIP = "businesstripAggregated",
    COMMUTING = "commutingAggregated",
    ELECTRICITY = "electricityAggregated",
    HEATING = "heatingAggregated"
}

const stableEmptyDataEntry = {
    emission: 0,
    perCapita: 0,
    date: undefined
}

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

const filterRawBackendDataForYear = (dataEntry: any, year: string) => {
    return dataEntry.filter((item: any) => new Date(item.date).getFullYear().toString() === year)    
}

export function mapChartData(rawData: any, year: string,  workingGroupSize: number = 1){
    const filtered_raw_data = {}
    Object.keys(rawData).forEach(key => filtered_raw_data[key] = filterRawBackendDataForYear(rawData[key], year))
    if(Object.keys(filtered_raw_data).map(key => filtered_raw_data[key]).every(dataCollection => dataCollection.length === 0)){
        return []
    }
    const mappedData = {
        "businessTotal" : mapBackendResult(filtered_raw_data[backendResultFields.BUSINESSTRIP]),
        "commutingTotal" : mapBackendResult(filtered_raw_data[backendResultFields.COMMUTING]),
        "electricityTotal": mapBackendResult(filtered_raw_data[backendResultFields.ELECTRICITY]),
        "heatingTotal": mapBackendResult(filtered_raw_data[backendResultFields.HEATING])
        }
        const chartData = months.map(month => {
            return createDataEntry(month, mappedData, workingGroupSize)
        })
        return chartData;
}


function createDataEntry(month: string, rawData: any, workingGroupSize: number): IChartDataEntry{
    const businessTripEntry = rawData.businessTotal?.find((businessTripEntry: IBusinessTripEntry) => businessTripEntry.date === month) ?? stableEmptyDataEntry
    const commutingEntry = rawData.commutingTotal?.find((commutingEntry: ICommutingEntry) => commutingEntry.date === month) ?? stableEmptyDataEntry
    const electricityEntry = rawData.electricityTotal?.find((electricityEntry: IElectricityEntry) => electricityEntry.date === month)  ?? stableEmptyDataEntry
    const heatingEntry = rawData.heatingTotal.find((heatingEntry: IHeatingEntry) => heatingEntry.date === month) ?? stableEmptyDataEntry;

    const sum = [businessTripEntry.emission, heatingEntry.emission, commutingEntry.emission, electricityEntry.emission].filter(item => item !== undefined).reduce((sum, current) => sum + current, 0)
    const avg = [businessTripEntry.perCapita, heatingEntry.perCapita, commutingEntry.perCapita, electricityEntry.perCapita].filter(item => item !== undefined).reduce((sum, current) => sum + current, 0)

    return {
        name: month, 
        business: businessTripEntry.emission,
        heating: heatingEntry.emission,
        commuting: commutingEntry.emission,
        electricity: electricityEntry.emission,
        sum: sum,
        max: 1000,
        totalMax: 1000*workingGroupSize,
        avg: Math.round(avg * 10) / 10
    }
}

function mapBackendResult(rawBackendResult: any){
    if ( rawBackendResult && rawBackendResult.length >= 1) {
        return rawBackendResult?.map((backendResultEntry: any) => {
            const datestring = backendResultEntry.date
            const month = format(new Date(datestring), 'LLLL');
            return {
                emission: backendResultEntry.co2e,
                perCapita: backendResultEntry.co2eCap, 
                date: month
            }
        })
    }
    else {
        return []
    }
}