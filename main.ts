import * as exceljs from 'exceljs';
import { Command } from 'commander';
import fs from 'fs/promises';
import { EXCEL_FILE_PATH } from './config'

// receive date and string value
const main = () => {
    const { table: bill, card } = init()

    if (!card || !bill) {
        throw Error('Incomplete required field')
    }

   analayzeSecBank(card, bill)
}

const init = () => {
    const program = new Command();

    program
        .name('cc-analyzer')
        .option('-b, --bank <string>', 'Bank')
        .option('-c --card <string>', 'Card')
        .option('-d, --date <string>', 'Statement Date')
        .option('-t, --table <string>', 'Statement table');

    program.parse();

    return program.opts()
}

const analayzeSecBank = async (card: string, bill: string) => {
    const split = bill.split('\\n');

    const data = split.map((s: any) => {
        const [transDate, postDate, ...rest] = s.split(' ');
        const merchant = rest.slice(0, rest.length - 1).join(' ')
        const amount = rest.pop();

        return {
            transDate,
            postDate,
            merchant,
            amount,
            skip: /PAYMENT - PHP\/SBC1/g.test(merchant),
            str: [transDate, postDate, merchant.replace(',', ''), amount.replace(',', '')].join(',')
        }
    })


    const d = new Date().toLocaleString('default', { month: 'short', year: "numeric" })
    const filename = `${d} ${card}.csv`;

    await fs.writeFile(`./dump/${filename}`, data.sort((a, b) => +new Date(a.transDate) - +new Date(b.transDate)).filter(d => !d.skip).map((d) => {
       return d.str
    }).join('\n'))
    console.log(data)
}

const excelReader = async () => {
    const workbook = new exceljs.Workbook();
    await workbook.xlsx.readFile(EXCEL_FILE_PATH);
}

main();