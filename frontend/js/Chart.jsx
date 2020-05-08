import React from 'react';
import { useTheme } from '@material-ui/core/styles';
import { LineChart, Line, XAxis, YAxis, Label, ResponsiveContainer, Tooltip, BarChart, Bar } from 'recharts';
import Title from './Title';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
    height: 360,
  },
}));

function CasesChart(props) {
  const theme = useTheme();
  const classes = useStyles();

  if (props.data.length === 0) {
    return null;
  }

  return (
    <Grid item xs={12}>
     <Paper className={classes.paper}>
      <Title>Number of cases over time</Title>
      <ResponsiveContainer>
        <LineChart
          data={props.data}
          width={850}
          margin={{
            top: 16,
            right: 16,
            bottom: 0,
            left: 24,
          }}
        >
          <XAxis dataKey="date" stroke={theme.palette.text.secondary} />
          <YAxis stroke={theme.palette.text.secondary}>
            <Label
              angle={270}
              position="left"
              style={{ textAnchor: 'middle', fill: theme.palette.text.primary }}
            >
              Confirmed Cases
            </Label>
          </YAxis>
          <Tooltip />
          <Line type="monotone" dataKey="count" stroke={theme.palette.primary.main} dot={false} />
        </LineChart>
      </ResponsiveContainer>
     </Paper>
    </Grid>
  );
}

function ChangeChart(props) {
  const theme = useTheme();
  const classes = useStyles();

  if (props.data.length === 0) {
    return null;
  }

  return (
    <Grid item xs={12}>
     <Paper className={classes.paper}>
      <Title>New cases over time</Title>
      <ResponsiveContainer>
        <BarChart
          data={props.data}
          width={850}
          margin={{
            top: 16,
            right: 16,
            bottom: 0,
            left: 24,
          }}
        >
          <XAxis dataKey="date" stroke={theme.palette.text.secondary} />
          <YAxis stroke={theme.palette.text.secondary}>
            <Label
              angle={270}
              position="left"
              style={{ textAnchor: 'middle', fill: theme.palette.text.primary }}
            >
              Confirmed Cases
            </Label>
          </YAxis>
          <Tooltip />
          <Bar type="monotone" dataKey="count" stroke={theme.palette.primary.main} dot={false} />
        </BarChart>
      </ResponsiveContainer>
     </Paper>
    </Grid>
  );
}

export{
    CasesChart,
    ChangeChart,
}