import * as exceljs from 'exceljs';
import { Command } from 'commander';
import { EXCEL_FILE_PATH } from './config'

// receive date and string value
const main = () => {
    const config = init()

    const split = config.table.split('\\n');

    const grouped = split.map((s: any) => {
        const [transDate, postDate, ...rest] = s.split(' ');
        const merchant = rest.slice(0, rest.length - 1).join(' ')

        return {
            transDate,
            postDate,
            merchant,
            amount: rest.pop()
        }
    })

    console.log(grouped)
}

const init = () => {
    const program = new Command();

    program
        .name('cc-analyzer')
        .option('-b, --bank <string>', 'Bank')
        .option('-d, --date <string>', 'Statement Date')
        .option('-t, --table <string>', 'Statement table');

    program.parse();

    return program.opts()
}

const excelReader = async () => {
    const workbook = new exceljs.Workbook();
    await workbook.xlsx.readFile(EXCEL_FILE_PATH);
}

main();